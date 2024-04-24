#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@ScriptName: assert_optimize.py
# @@Author: 张砚程
# @@Create Date: 2021-03-25 22:24:14
# @@Modify Date: 2012-93-25 22:24:34
# @@Description: 优化断言，相等、包含、存在
# @@Copyright © 91duobaoyu, Inc. All rights reserved.
# *********************************************************#

import time
import pytest
from public.log import Log
import pytest_assume

def new_assert_equal(contents, expects, actuals):
    """
    校验实际和期望值相等
    """
    actual, expect = str(actuals), str(expects)
    try:
        pytest.assume(expect == actual)
        if expect == actual:
            result = 'true'
            Log().info('对【{}】断言，结果：预期值 {} == 实际值 {}，断言成功'.format(contents, expect, actual))
        elif expect != actual:
            result = 'false'
            Log().warning('对【{}】断言，结果：预期值 {} != 实际值 {}，断言失败'.format(contents, expect, actual))
        else:
            result = 'false'
            Log().warning('断言失败')
    finally:
        return result

def new_assert_notequal(contents, expects, actuals):
    """
    校验实际和期望值不相等
    """
    actual, expect = str(actuals), str(expects)
    try:
        pytest.assume(expect != actual)
        if expect != actual:
            Log().info('对【{}】断言，结果：预期值 {} != 实际值 {}，断言成功'.format(contents, expect, actual))
        elif expect == actual:
            Log().warning('对【{}】断言，结果：预期值 {} == 实际值 {}，断言失败'.format(contents, expect, actual))
            raise '断言失败'
        else:
            Log().warning('断言失败')
            raise '断言失败'
    except:
        raise '断言失败'

def new_assert_exist(contents, actuals):
    """
    判断实际值存在
    :param content: 断言字段名
    :param actual: 实际值
    :return:
    """
    actual = str(actuals)
    try:
        if actual == '' or actual == '[]':
            Log().warning('【{}】不存在，值为空，断言失败'.format(contents))
            raise '断言失败'
        else:
            assert actual
            Log().info('【{}】存在，值为【{}】，断言成功'.format(contents, actual))
    except:
        raise '断言失败'

def new_assert_contains(contens, expects, actuals):
    """
    判断期望值在实际值里存在
    """
    actual, expect = str(actuals), str(expects)
    try:
        if expect in actual:
            Log().info('对【{}】断言，期望值【{}】在实际值【{}】内，断言成功'.format(contens, expect, actual))
        elif expect not in actual:
            Log().warning('对【{}】断言，期望值【{}】不在实际值【{}】内，断言失败'.format(contens, expect, actual))
            raise '断言失败'
        else:
            Log().warning('断言失败')
            raise '断言失败'
    except:
        raise '断言失败'

def new_assert_notcontains(contens, expects, actuals):
    """
    判断期望值在实际值里不存在
    """
    actual, expect = str(actuals), str(expects)
    try:
        if expect in actual:
            result = 'false'
            Log().warning('对【{}】断言，期望值【{}】在实际值【{}】内，断言失败'.format(contens, expect, actual))
            raise
        elif expect not in actual:
            result = 'true'
            Log().info('对【{}】断言，期望值【{}】不在实际值【{}】内，断言成功'.format(contens, expect, actual))
        else:
            result = 'false'
            Log().warning('断言失败')
    finally:
        return result

if __name__ == "__main__":
    list= [{'detailNo': '261045783602794496', 'title': '积分扣减通知', 'body': '您好，周雅(FS001287)，您有1000积分已扣减！', 'isRead': 0, 'fsUserId': None, 'pushTime': '2021-08-19 17:22:45', 'pushTimeTimeStamp': 1629364965000, 'msgDetailJump': 'none', 'msgDetailJumpExt': None, 'msgDetailJumpExtMap': None}, {'detailNo': '261044444688683008', 'title': '积分扣减通知', 'body': '您好，周雅(FS001287)，您有1000积分已扣减！', 'isRead': 0, 'fsUserId': None, 'pushTime': '2021-08-19 17:17:26', 'pushTimeTimeStamp': 1629364646000, 'msgDetailJump': 'none', 'msgDetailJumpExt': None, 'msgDetailJumpExtMap': None}]
    list1=[]
    count = 0
