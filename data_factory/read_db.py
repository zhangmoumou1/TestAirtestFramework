#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: zhangmoumou
# @@Create Date: 2021-03-25 22:24:14
# @@Modify Date: 2012-93-25 22:24:34
# @@Description: mysql相关操作
# *********************************************************#

import datetime
import pymysql
import re
import platform
import time
from public.log import Log
from branch.read_yaml import ReadYaml
from branch import globalparam
from dbutils.pooled_db import PooledDB
from sshtunnel import SSHTunnelForwarder
# from DBUtils.PooledDB import PooledDB
from branch.read_yaml import ReadYaml


ENV = globalparam.environment
SYSTEM_VERSION = platform.platform()

class MysqlStructure(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None
    testdata_mysql_name = 'testdata_mysql'

    @staticmethod
    def __get_conn(db_name, db_info):
        """
        从连接池中取出连接
        :param db_name: 数据库名称
        :param db_info: 连接信息
        :return: MySQLdb.connection
        :当环境为非Linux环境，使用ssh连接
        """
        try:
            server = SSHTunnelForwarder(
                ssh_address_or_host=('jms.91duobaoyu.com', 2221),
                ssh_username=('rdspass'),
                ssh_password=('1aqz#DEC'),
                remote_bind_address=(db_info[0], db_info[1]))

            server.start()
            connect = pymysql.connect(
                user=db_info[2],
                passwd=db_info[3],
                host='127.0.0.1',
                db=db_name,
                port=server.local_bind_port
            )
            return connect
        except Exception as e:
            Log().error('连接{}数据库失败，请检查连接信息是否正确：{}'.format(db_name, e))
            raise


    @staticmethod
    def select_mysql_results(db_name, sql):
        """
        操作业务数据库表，增删改查操作,返回单/多个字段和记录
        :return: {"key": "value"} 或 [{"key1": "value1"},{"key2": "value2"}]
        """
        try:
            # 获取MySQL连接信息，创建连接
            db_info = ['rm-bp12ojz0ytip70e27.mysql.rds.aliyuncs.com', 3306, 'qateam', 'qz844972by']
            _conn = MysqlStructure.__get_conn(db_name, db_info)
            _cursor = _conn.cursor()
            if 'user_entry_apply_approval' in sql:
                # 针对表user_entry_apply_approval的approval_status的状态不做处理，因为值为大写
                __sql = sql
            else:
                __sql = sql.lower().strip()
            Log().info('成功登录{}环境{}数据库，执行SQL：{}'.format(ENV, db_name, __sql))
            _cursor.execute(__sql)
            results = _cursor.fetchall()
            sql1 = __sql.replace(' ', '')
            if len(re.findall("^select", __sql)) == 1:
                # 执行查询操作
                find_keys = re.findall("^select(.+?)from", sql1)
                # 校验sql查询结果是表的全量*字段还是部分字段
                if '*' == find_keys[0]:
                    del_null_sql = __sql.replace(' ', '')
                    find_table_name = re.findall("from(.+?)$", del_null_sql)
                    # 校验sql，从里面取出表名
                    if 'where' in find_table_name[0]:
                        table_name = re.findall("from(.+?)where", del_null_sql)[0]
                    else:
                        table_name = find_table_name[0]
                    __column_name_sql = 'select COLUMN_NAME from information_schema.COLUMNS where table_name = ' \
                                        '"{}" and table_schema = "{}";'.format(table_name, db_name)
                    _cursor.execute(__column_name_sql)
                    key_results = _cursor.fetchall()
                    _cursor.execute(__sql)
                    value_results = _cursor.fetchall()
                    if len(value_results) == 0:
                        return None
                    else:
                        dict_results = {}
                        for number in range(len(key_results)):
                            key, value = key_results[number][0], value_results[0][number]
                            dict_results[key] = value
                        Log().info("表{}的sql查询结果：{}".format(table_name, dict_results))
                        return dict_results
                else:
                    keys = find_keys[0].split(",")
                    list_result = []
                    dict_result = {}
                    # 处理单个结果，单个结果为字典{结果}
                    if len(results) == 1:
                        for i in results:
                            for num in range(len(i)):
                                # 处理连接查询字段处理，如a.id
                                if '.' in keys[num] and 'join' in sql1:
                                    key = keys[num].split('.')[-1]
                                else:
                                    key = keys[num]
                                # 如果查询结果是datetime类型，处理成str
                                if isinstance(i[num], datetime.datetime):
                                    dict_result[key] = str(i[num])
                                else:
                                    dict_result[key] = i[num]
                                list_result.append(dict_result)
                        Log().info('sql查询结果：{0}'.format(dict_result))
                        results = dict_result
                        return results
                    # 处理多个结果，多个结果为数组[{结果1},{结果2}]
                    elif len(results) > 1:
                        for i in results:
                            dict_result1 = {}
                            for num in range(len(i)):
                                # 处理连接查询字段处理，如a.id
                                if '.' in keys[num] and 'join' in sql1:
                                    key = keys[num].split('.')[-1]
                                else:
                                    key = keys[num]
                                if isinstance(i[num], datetime.datetime):
                                    dict_result1[key] = str(i[num])
                                else:
                                    dict_result1[key] = i[num]
                                list_result.append(dict_result1)
                        results = list_result
                        Log().info('sql查询结果：{0}'.format(list_result))
                        return results

            elif len(re.findall("^delete", __sql)) == 1:
                # 执行删除操作
                _conn.commit()
                Log().info('sql删除数据成功：{0}'.format(sql))
            elif len(re.findall("^insert into", __sql)) == 1:
                # 执行新增操作
                _conn.commit()
                Log().info('sql新增数据成功：{0}'.format(sql))
            elif len(re.findall("^update", __sql)) == 1:
                # 执行更新操作
                _conn.commit()
                Log().info('sql更新数据成功：{0}'.format(sql))
            _conn.close()
        except Exception as e:
            Log().error("执行sql：{}，数据库查询失败，请检查sql格式是否书写正确：{}".format(sql, e))
            raise

    @staticmethod
    def handle_mysql(key, name):
        """
        业务库操作
        """
        # 仅限预发环境执行
        if ENV == 'PRE':
            for info in ReadYaml().get_factory_db(key, name):
                MysqlStructure.select_mysql_results(info[0], info[1])


if __name__ == "__main__":
    MysqlStructure.handle_mysql('zhangyancheng', 'sql1')