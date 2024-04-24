#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: zhangmoumou
# @@Create Date: 2021-03-25 22:24:14
# @@Modify Date: 2012-93-25 22:24:34
# @@Description: 读取config.ini配置数据，进行处理
# *********************************************************#

import configparser
import os

config_file_path = os.path.split(os.path.realpath(__file__))[0]
FILENAME = os.path.join(config_file_path, '../conf/config.ini')

class ReadConfig(object):
    """
    读取config.ini配置文件
    return：value
    """
    def __init__(self):
        self.configpath = FILENAME
        self.cf = configparser.ConfigParser()

    def getValue(self, env, name):
        """
        读取config.ini文件
        :param env:
        :param name:
        :return:
        """
        try:
            self.cf.read(self.configpath, encoding='utf-8')
            results = self.cf.get(env, name)
            return results
        except Exception as e:
            raise

if __name__ == "__main__":
    environment = ReadConfig().getValue('envConfig', 'environment')
