# -*- coding: utf-8 -*-
# @desc     : 获取用例执行结果，并发送至钉钉

import sys
import os
import time
import platform
import uuid

curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
# from branch.send_ding import send_msg
from public.methods import *
ENV = globalparam.environment
SYSTEM_VERSION = platform.platform()
UUID = uuid.UUID(int=uuid.getnode())


def pytest_terminal_summary(terminalreporter):
    """将运行结果发送至钉钉和预发用例统计数据"""
    cases = terminalreporter._numcollected
    case_pass = len(terminalreporter.stats.get('passed', []))
    case_fail = len(terminalreporter.stats.get('failed', []))
    case_error = len(terminalreporter.stats.get('error', []))
    case_skip = len(terminalreporter.stats.get('skipped', []))
    case_time = round(time.time() - terminalreporter._sessionstarttime, 2)
    # 远程服务器执行，才发送钉钉通知
    if str(UUID) == '00000000-0000-0000-0000-00e269232fe5':
        # send_msg(cases, case_pass, case_fail, case_error, case_skip, case_time)
        from run_config.run_end import update_result
        update_result(cases, case_pass, case_fail + case_error, case_skip, case_time)
        if (case_fail + case_error) > 0:
            # 为了让Jenkins抛错
            fail = terminalreporter.stats.get('failed', []) + terminalreporter.stats.get('error', [])
            raise f'存在失败用例，{fail}'

