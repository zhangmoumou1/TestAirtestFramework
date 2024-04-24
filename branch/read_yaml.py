#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: zhangmoumou
# @@Create Date: 2021-03-25 22:24:14
# @@Modify Date: 2012-93-25 22:24:34
# @@Description: yaml文件相关操作
# *********************************************************#

import os, sys
import yaml
import platform
import uuid
from public.log import Log
from branch import globalparam

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# 获取当前脚本所在文件夹路径
ENV = globalparam.environment
SYSTEM_VERSION = platform.platform()
UUID = uuid.UUID(int=uuid.getnode())
CURPATH = os.path.dirname(os.path.realpath(__file__))
URL_PATH = os.path.join(CURPATH, "../conf/url_user.yaml")
DB_PATH = os.path.join(CURPATH, "../conf/db.yaml")

data_db = os.path.join(CURPATH, "../data_factory/db.yaml")
data_http = os.path.join(CURPATH, "../data_factory/http.yaml")

class ReadYaml(object):
    """
    读取操作yaml文件
    """
    def __init__(self, project=True):
        self.project = project
        self._url_path = URL_PATH
        self._db_path = DB_PATH
        self._data_db = data_db
        self._data_http = data_http

    def get_url_user(self, key):
        """
        获取不同环境的url、user/pwd、token
        :param key: app_url/wx_token/wms_url/wms_user_pwd
        :return:
        """
        try:
            with open(self._url_path, 'rb') as f:
                cont = f.read()
            cf = yaml.load(cont, Loader=yaml.FullLoader)
            data = cf.get('baoyutong')[ENV][key]
            return data
        except Exception as e:
            Log().error("查询yaml文件url/user/token失败：{}".format(e))

    def get_redis(self, env='TEST'):
        """
        找到yaml中对应的redis连接信息
        :return: [ip, port, 密码]
        """
        try:
            with open(self._db_path, 'rb') as f:
                cont = f.read()
            cf = yaml.load(cont, Loader=yaml.FullLoader)
            data = cf.get(env)['redis_info']
            print(data)
            if 'Linux' in SYSTEM_VERSION:
                del data[0]
                return data
            else:
                del data[1]
                return data
        except Exception as e:
            Log().error("查询yaml文件数据库连接信息失败：{}".format(e))
            raise

    def get_factory_db(self, name, key):
        """
        获取执行sql
        """
        with open(self._data_db, 'rb') as f:
            cont = f.read()
        cf = yaml.load(cont, Loader=yaml.FullLoader)
        data = cf.get(name)[key]
        for sql in data:
            yield sql.split("#")

    def get_factory_http(self, name, key):
        with open(self._data_http, 'rb') as f:
            cont = f.read()
        cf = yaml.load(cont, Loader=yaml.FullLoader)
        data = cf.get(name)[key]
        return data

if __name__ == "__main__":
    aa = ReadYaml().get_factory_http('zhangyancheng', 'http1')
    print(aa)
    # ReadYaml().get_redis('PRE')
    # ReadYaml().get_factory_db('zhangyancheng', 'sql1')