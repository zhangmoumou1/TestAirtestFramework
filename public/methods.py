#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: zhangmoumou
# @@Create Date: 2021-03-25 22:24:14
# @@Modify Date: 2012-93-25 22:24:34
# @@Description: 集合可调用方法，统一调用即可
# *********************************************************#

import time
import pytest
import platform
import allure
import requests
import datetime
from time import sleep
from branch import globalparam
from public.assert_optimize import new_assert_equal, new_assert_notequal, new_assert_exist, \
    new_assert_contains, new_assert_notcontains
from public.log import Log
from public.base import PocoPackage, PocoPackageFx
from testcase.baoyutong_page_obj.yxx_login import LoginPage
from branch.read_yaml import ReadYaml
from data_factory.read_db import MysqlStructure
from data_factory.http_structure import HttpStructure
from public.commom_operation import CommonOperation

SYSTEM_VERSION = platform.platform()

__all__ = [
    'pytest',
    'allure',
    'sleep',
    'globalparam',
    'new_assert_equal',
    'new_assert_notequal',
    'new_assert_exist',
    'new_assert_contains',
    'new_assert_notcontains',
    'PocoPackage',
    'PocoPackageFx',
    'LoginPage',
    'Log',
    'time',
    'ReadYaml',
    'requests',
    'MysqlStructure',
    'HttpStructure',
    'CommonOperation',
    'datetime'
]