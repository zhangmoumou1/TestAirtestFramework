#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: zhangmoumou
# @@Create Date: 2021-08-3 14:24:14
# @@Modify Date: 2022-08-30 14:24:34
# @@Description: redis相关操作
# *********************************************************#
import platform
import random
import redis
from sshtunnel import SSHTunnelForwarder
from branch import globalparam
from public.log import Log
from branch.read_yaml import ReadYaml


ENV = globalparam.environment

SYSTEM_VERSION = platform.platform()

class OperateRedis(object):
    """执行redis操作"""

    def __init__(self, project='interface'):
        self.project = project
        self.env = ENV
        if ENV == 'PRE' or ENV == 'RELEASE':
            self.conn_pre = OperateRedis.__get_conn_redis(ENV)
        else:
            self.conn = OperateRedis.__get_conn_redis()
    @staticmethod
    def __get_conn_redis(env='TEST'):
        """
        从连接池中取出连接
        :param db_name: 数据库名称
        :param db_info: 连接信息
        :return: redisdb.connection
        :当环境为非Linux环境，使用隧道连接
        """
        try:
            # 判断本地系统，如果是win或mac系统，使用ssh登录
            if env == 'PRE':
                db_info = ReadYaml().get_redis(env=env)
            elif env == 'RELEASE':
                db_info = ReadYaml().get_redis(env=env)
            else:
                db_info = ReadYaml().get_redis(env=env)
            if 'Linux' in SYSTEM_VERSION:
                redis_con = redis.Redis(host=db_info[0], port=db_info[1], password=db_info[2], db=db_info[3])
                return redis_con
            else:
                server = SSHTunnelForwarder(
                    ssh_address_or_host=('jms.91duobaoyu.com', 2221),
                    ssh_username='rdspass',
                    ssh_password='1aqz#DEC',
                    local_bind_address=('localhost', random.randint(1000, 9999)),
                    remote_bind_address=(db_info[0], 6379))

                server.start()
                redis_con = redis.Redis(
                    host='localhost',
                    port=server.local_bind_port,
                    db=db_info[3],
                    password=db_info[2],
                    decode_responses=True
                )
                return redis_con
        except Exception as e:
            Log().info('redis连接失败，请检查连接信息是否正确：{}'.format(e))
            raise


    def handle_redis(self, type, action, *args):
        """
        对业务redis进行增删改查操作，用到new_requests.py，分为字符串、列表、哈希、集合类型
        :return:
        """
        try:
            if action == 'delete':
                # 删除整个键值
                self.conn_pre.delete(args[0][0])
                result = True
            else:
                if type == 'str':
                    if action in ['add', 'update']:
                        result = self.conn_pre.set(args[0][0], args[0][1])
                    elif action == 'select':
                        result = self.conn_pre.get(args[0][0])
                        return result
                elif type == 'list':
                    if action in ['add', 'update']:
                        result = self.conn_pre.lpush(args[0][0], args[0][1])
                    elif action == 'select':
                        result = self.conn_pre.lindex(args[0][0], args[0][1])
                        return result
                elif type == 'hash':
                    if action in ['add', 'update']:
                        result = self.conn_pre.hset(args[0][0], args[0][1], args[0][2])
                    elif action == 'select':
                        result = self.conn_pre.hget(args[0][0], args[0][1])
                        return result
                    elif action == 'hdelete':
                        result = self.conn_pre.hdel(args[0][0], args[0][1])
                elif type == 'set':
                    pass
                else:
                    raise 'redis类型写法有误：{}'.format(type)
        except:
            Log().error('操作业务redis的{}类型数据，对键名【{}】进行{}操作失败：请查看写法是否正确!')
            raise
        finally:
            Log().info('操作业务redis的{}类型数据，对键名【{}】进行{}操作成功，执行结果：{}'.format(type, args[0], action, result))


if __name__ == "__main__":
    conn = OperateRedis()
    conn.handle_redis('str', 'select', ['13714390524'])