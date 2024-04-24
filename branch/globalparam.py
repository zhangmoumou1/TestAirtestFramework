#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: zhangmoumou
# @@Create Date: 2022-09-25 22:24:14
# @@Modify Date: 2022-09-25 22:24:34
# @@Description: 子目录写入环境变量
# *********************************************************#


import os
from branch.read_config import ReadConfig
# 读取配置文件路径
prj_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
read_config = ReadConfig()

# 读取配置文件里的参数
environment = read_config.getValue('envConfig', 'environment')
ding_token_1 = read_config.getValue('dingConfig', 'ding_token_1')
ding_token_2 = read_config.getValue('dingConfig', 'ding_token_2')
ding_token_3 = read_config.getValue('dingConfig', 'ding_token_3')
ding_token_4 = read_config.getValue('dingConfig', 'ding_token_4')
ding_token_5 = read_config.getValue('dingConfig', 'ding_token_5')
ding_token_6 = read_config.getValue('dingConfig', 'ding_token_6')

# Log path
log_path = os.path.join(prj_path, 'report', 'logs')
picture_path = os.path.join(prj_path, 'report', 'pictures')
ocr_path = os.path.join(prj_path, 'report', 'ocr')
file_path = os.path.join(prj_path, 'static_files')
pic_locate_path = os.path.join(prj_path, 'pictures', 'locate_picture')
pic_assert_path = os.path.join(prj_path, 'pictures', 'assert_picture')
error_file = os.path.join(prj_path, 'report')


if __name__ == "__main__":
    print(prj_path)
