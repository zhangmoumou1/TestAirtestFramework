#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: zhangmoumou
# @@Create Date: 2022-09-25 22:24:14
# @@Modify Date: 2022-09-25 22:24:34
# @@Description: 拓展功能
# *********************************************************#

import time
import re
import json
import os
import requests
import redis
import platform
import random
import string
import datetime
import calendar
from branch.read_redis import OperateRedis
from branch import globalparam
from sshtunnel import SSHTunnelForwarder
from public.log import Log
from branch.read_yaml import ReadYaml
from dingtalkchatbot.chatbot import DingtalkChatbot

ENV = globalparam.environment

SYSTEM_VERSION = platform.platform()

redis_con = OperateRedis()

def DealWithTime(values='{{分截止+2d}}'):
    """
    处理用例中格式为{{xxx}}的数据
    params：{{分截止+2m}}
    return：年-月-日 时:分:秒 或 年-月-日 时:分
    """
    try:
        global param
        param = values
        if values == None:
            return param
        elif 'DATA' in param:
            return param
        elif ('{{' in values) and ('}}' in values):
            # 取出{{}}内的值
            time_list = re.findall("{{(.+?)}}", values)
            for time_value in time_list:
                # 解析填充手机号
                if 'mobile' in time_value:
                    # 如果存在. 说明需要存入redis做为全局变量
                    if '.mobile' in time_value:
                        redis_key = time_value.split('.')[0]
                        mobile = generate_mobile()
                        param = param.replace('{{' + time_value + '}}', mobile)
                        # redis插入全局变量
                        redis_con.insert_redis_data(redis_key, mobile)
                    else:
                        param = param.replace('{{mobile}}', generate_mobile())
                # 解析填充随机数
                if 'number' in time_value:
                    if '-' in time_value:
                        data1 = time_value.split('number')[-1]
                        data2 = data1.split('-')
                        start, end = int(data2[0]), int(data2[1])
                        number = str(random_with_long(start, end))
                        param = param.replace('{{' + time_value + '}}', number)
                        # redis插入全局变量
                        if '.number' in time_value:
                            redis_key = time_value.split('.')[0]
                            redis_con.insert_redis_data(redis_key, number)
                    else:
                        data = time_value.split('number')[-1]
                        number = str(random_with_long1(int(data)))
                        param = param.replace('{{' + time_value + '}}', number)
                        # redis插入全局变量
                        if '.number' in time_value:
                            redis_key = time_value.split('.')[0]
                            redis_con.insert_redis_data(redis_key, number)
                # 指定时间，如每个月1号，写法为{{指定月01日}}
                if '指定' in time_value:
                    # 时间为年-月-日 时:分:秒
                    now_time = datetime.datetime.now()
                    time_list = [['分', '秒'], ['时', '分'], ['日', '时'], ['月', '日'], ['指定', '月']]
                    # 替换月、日、时、分、秒
                    months, days, hours, minutes, seconds = 0, 0, 0, 0, 0
                    for time1 in time_list:
                        expect_seconds = re.findall("{0}(.+?){1}".format(time1[0], time1[1]), time_value)
                        if time1[1] == '秒':
                            if expect_seconds == []:
                                seconds = now_time.second
                            elif expect_seconds != []:
                                seconds = int(expect_seconds[0])
                        elif time1[1] == '分':
                            if expect_seconds == []:
                                minutes = now_time.minute
                            elif expect_seconds != []:
                                minutes = int(expect_seconds[0])
                        elif time1[1] == '时':
                            if expect_seconds == []:
                                hours = now_time.hour
                            elif expect_seconds != []:
                                hours = int(expect_seconds[0])
                        elif time1[1] == '日':
                            if expect_seconds == []:
                                days = now_time.day
                            elif expect_seconds != []:
                                days = int(expect_seconds[0])
                        elif time1[1] == '月':
                            if expect_seconds == []:
                                months = now_time.month
                            elif expect_seconds != []:
                                months = int(expect_seconds[0])
                    if '秒' in time_value:
                        time2 = str(datetime.datetime(month=months, year=now_time.year, day=days,
                                                  hour=hours, minute=minutes, second=seconds))
                    elif ('秒' not in time_value) and ('分' in time_value):
                        time2 = str(datetime.datetime(month=months, year=now_time.year, day=days,
                                                  hour=hours, minute=minutes)).replace(':00', '')
                    elif ('分' not in time_value) and ('时' in time_value):
                        time2 = str(datetime.datetime(month=months, year=now_time.year, day=days,
                                                      hour=hours)).replace(':00:00', '')
                    elif ('时' not in time_value) and ('日' in time_value):
                        time2 = str(datetime.datetime(month=months, year=now_time.year, day=days)).replace(' 00:00:00', '')
                    param = param.replace('{{' + time_value + '}}', time2)

                # 查询业务redis
                if 'redis' in time_value:
                    all = time_value.split('.')
                    end_args = all[3:]
                    result = redis_con.handle_redis(all[1], all[2], end_args)
                    param = param.replace('{{' + time_value + '}}', result)

                # 解析填充时间
                else:
                    now_time = datetime.datetime.now()
                    if '+' in time_value:
                        value = time_value.split('+')
                        number = int(value[-1][:-1])
                        if value[0] == '秒截止':
                            if 's' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + number))
                            elif 'm' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + number * 60))
                            elif 'h' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + number * 3600))
                            elif 'd' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + number * 3600 * 24))
                            elif 'M' in value[1]:
                                time1 = datetime.datetime(month=now_time.month + number, year=now_time.year,
                                                          day=now_time.day, hour=now_time.hour, minute=now_time.minute)
                                times = time1.strftime('%Y-%m-%d %H:%M:%S')
                            elif 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year + number,
                                                          day=now_time.day, hour=now_time.hour, minute=now_time.minute)
                                times = time1.strftime('%Y-%m-%d %H:%M:%S')
                        elif value[0] == '分截止':
                            if 's' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + number))
                            elif 'm' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + number * 60))
                            elif 'h' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + number * 3600))
                            elif 'd' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() + number * 3600 * 24))
                            elif 'M' in value[1]:
                                time1 = datetime.datetime(month=now_time.month + number, year=now_time.year,
                                                               day=now_time.day, hour=now_time.hour, minute=now_time.minute)
                                times = time1.strftime('%Y-%m-%d %H:%M')
                            elif 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year + number,
                                                          day=now_time.day, hour=now_time.hour, minute=now_time.minute)
                                times = time1.strftime('%Y-%m-%d %H:%M')

                        elif value[0] == '日截止':
                            if 'd' in value[1]:
                                times = time.strftime('%Y-%m-%d', time.localtime(time.time() + number * 3600 * 24))
                            elif 'M' in value[1]:
                                time1 = datetime.datetime(month=now_time.month + number, year=now_time.year,
                                                          day=now_time.day)
                                times = time1.strftime('%Y-%m-%d')
                            elif 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year + number,
                                                          day=now_time.day)
                                times = time1.strftime('%Y-%m-%d')
                        elif value[0] == '月截止':
                            if 'M' in value[1]:
                                # 获取指定月的天数，可能会存在超出天数的情况
                                monthRange = calendar.monthrange(now_time.year, now_time.month - number)
                                if monthRange[-1] < now_time.day:
                                    day = monthRange[-1]
                                else:
                                    day = now_time.day
                                time1 = datetime.datetime(month=now_time.month + number, year=day,
                                                          day=now_time.day)
                                times = time1.strftime('%Y-%m')
                            elif 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year + number,
                                                          day=now_time.day)
                                times = time1.strftime('%Y-%m')
                        elif value[0] == '年截止':
                            if 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year + number,
                                                          day=now_time.day)
                                times = time1.strftime('%Y')
                        param = param.replace('{{' + time_value + '}}', times)
                    elif '-' in time_value:
                        value = time_value.split('-')
                        number = int(value[-1][:-1])
                        if value[0] == '秒截止':
                            if 's' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - number))
                            elif 'm' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - number * 60))
                            elif 'h' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - number * 3600))
                            elif 'd' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M:%S',
                                                      time.localtime(time.time() - number * 3600 * 24))
                            elif 'M' in value[1]:
                                time1 = datetime.datetime(month=now_time.month - number, year=now_time.year,
                                                          day=now_time.day, hour=now_time.hour, minute=now_time.minute)
                                times = time1.strftime('%Y-%m-%d %H:%M:%S')
                            elif 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year - number,
                                                          day=now_time.day, hour=now_time.hour, minute=now_time.minute)
                                times = time1.strftime('%Y-%m-%d %H:%M:%S')
                        elif value[0] == '分截止':
                            if 's' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - number))
                            elif 'm' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - number * 60))
                            elif 'h' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - number * 3600))
                            elif 'd' in value[1]:
                                times = time.strftime('%Y-%m-%d %H:%M',
                                                      time.localtime(time.time() - number * 3600 * 24))
                            elif 'M' in value[1]:
                                time1 = datetime.datetime(month=now_time.month - number, year=now_time.year,
                                                          day=now_time.day, hour=now_time.hour, minute=now_time.minute)
                                times = time1.strftime('%Y-%m-%d %H:%M')
                            elif 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year - number,
                                                          day=now_time.day, hour=now_time.hour, minute=now_time.minute)
                                times = time1.strftime('%Y-%m-%d %H:%M')

                        elif value[0] == '日截止':
                            if 'd' in value[1]:
                                times = time.strftime('%Y-%m-%d', time.localtime(time.time() - number * 3600 * 24))
                            elif 'M' in value[1]:
                                time1 = datetime.datetime(month=now_time.month - number, year=now_time.year,
                                                          day=now_time.day)
                                times = time1.strftime('%Y-%m-%d')
                            elif 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year - number,
                                                          day=now_time.day)
                                times = time1.strftime('%Y-%m-%d')
                        elif value[0] == '月截止':
                            if 'M' in value[1]:
                                # 获取指定月的天数，可能会存在超出天数的情况
                                monthRange = calendar.monthrange(now_time.year, now_time.month - number)
                                if monthRange[-1] < now_time.day:
                                    day = monthRange[-1]
                                else:
                                    day = now_time.day
                                time1 = datetime.datetime(month=now_time.month - number, year=now_time.year, day=day)
                                times = time1.strftime('%Y-%m')
                            elif 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year - number,
                                                          day=now_time.day)
                                times = time1.strftime('%Y-%m')
                        elif value[0] == '年截止':
                            if 'Y' in value[1]:
                                time1 = datetime.datetime(month=now_time.month, year=now_time.year - number,
                                                          day=now_time.day)
                                times = time1.strftime('%Y')
                        param = param.replace('{{' + time_value + '}}', times)
            return param
        else:
            return values
    except Exception as e:
        Log().error('固定值获取失败，请检查书写格式是否正确：{}，如{{xxxx}}'.format(e))
        raise

def check_single_id(ids):
    """
    校验存在一个用例id区间
    """
    try:
        if '#' in ids.replace('zyc-', ''):
            id_str = ''
            bb = ids.split('#')
            point_start = bb[0].split('.')[0]
            point_end = bb[1]
            start = int(bb[0].split('.')[1])
            num = int(bb[1].split('.')[1]) - int(bb[0].split('.')[1])
            for i in range(num):
                ids = point_start + '.' + str(start + i)
                id_str += (ids + ',')
            return (id_str + point_end)
        else:
            return ids
    except:
        raise

def deal_with_caseid(case_id):
    """
    处理用例id，整合成zyc-1.1、zyc-1.2...
    """
    try:
        if ',' in case_id.replace(' ', '') and '#' in case_id.replace(' ', ''):
            id_all = ''
            for aa in case_id.split(','):
                id_all += check_single_id(aa) + ','
            if id_all[-1] == ',':
                id_result = id_all[:-1]
            return id_result
        else:
            return check_single_id(case_id)
    except:
        raise

class StatisticalCoverage(object):
    """
    统计接口覆盖率，用于钉钉消息
    """
    def __init__(self):
        self.url = 'http://swagger.91duobaoyu.com/api'
        self.header = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.101 Safari/537.36'
        }

    def get_service_path(self):
        """
        获取服务地址路径
        """
        url = 'http://swagger.91duobaoyu.com/api/swagger-resources'
        try:
            res = requests.get(url, self.header)
            for path in json.loads(res.text):
                yield path['url']
        except Exception as e:
            Log().error('获取swagger服务路径失败：{}'.format(e))
            raise

    def swagger_number(self):
        """
        swagger接口数量
        """
        try:
            base_number = 0
            for path in self.get_service_path():
                res = requests.get(url=self.url + path, headers=self.header)
                if res.status_code != 200:
                    continue
                if 'paths' not in json.loads(res.text):
                    continue
                single_number = len(json.loads(res.text)['paths'])
                base_number += single_number
            return base_number
        except Exception as e:
            Log().error('获取接口数量失败：{}'.format(e))
            raise

    def accounted_cases(self):
        """
        已写的接口数量
        """
        redis_con = OperateRedis()
        try:
            local_cases = float(redis_con.select_redis_data('pass_case_number'))
            swagger_cases = float(self.swagger_number())
            accounted_case = "%.1f%%" % (local_cases / swagger_cases*100)
            return accounted_case
        except Exception as e:
            Log().error('计算覆盖率失败：{}'.format(e))
            raise

class SelectSms(object):
    """
    查询验证码，线上环境
    """
    def __init__(self, project='interface'):
        self.project = project
        self.env = ENV
        self.conn = SelectSms.__get_conn_redis()

    @staticmethod
    def __get_conn_redis():
        """
        创建连接信息
        """
        try:
            # 判断本地系统，如果是win或mac系统，使用ssh登录
            db_info = ReadYaml().get_redis(env='RELEASE')
            if 'Linux' in SYSTEM_VERSION:
                redis_con = redis.Redis(host=db_info[0], port=db_info[1], password=db_info[2], db=db_info[3])
                return redis_con
            else:
                server = SSHTunnelForwarder(
                    ssh_address_or_host=('jms.91duobaoyu.com', 2221),
                    ssh_username='rdspass',
                    ssh_password='1aqz#DEC',
                    local_bind_address=('localhost', 6380),
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
            raise

    def select_redis_sms(self, mobile):
        """
        获取验证码，线上环境
        """
        try:
            result = self.conn.get(mobile)
            if 'Linux' in SYSTEM_VERSION:
                return result.decode('UTF-8').replace('"', "")
            else:
                return result.replace('"', "")
        except Exception as e:
            Log().error("{}环境，查看手机号验证码[key：{}]失败：{}".format(ENV, mobile, e))

def generate_mobile():
    """
    随机生成手机号
    return：12356345636
    """
    prefix = [
        '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
        '145', '147', '149', '150', '151', '152', '153', '155', '156', '157',
        '158', '159', '165', '171', '172', '173', '174', '175', '176', '177',
        '178', '180', '181', '182', '183', '184', '185', '186', '187', '188',
        '189', '191'
    ]
    pos = random.randint(0, len(prefix) - 1)
    suffix = ''.join(random.sample(string.digits, 8))
    return prefix[pos] + suffix

def random_with_long(start, end):
    """
    根据指定区间生成数字随机数
    """
    try:
        return random.randint(start, end)
    except:
        Log().error('生成区间数字随机数失败')

def random_with_long1(n):
    """
    生成指定长度的数字随机数
    """
    try:
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start, range_end)
    except:
        Log().error('生成指定长度数字随机数失败')

def skip_release():
    """
    RELEASE环境不执行，测试脚本中使用
    """
    def wrapper(func):
        def deco(*args, **kwargs):
            if ENV == 'RELEASE':
                Log().error('当前为RELEASE环境，执行失败')
            else:
                func(*args, **kwargs)
        return deco
    return wrapper

def statistics_pre_cases(case_id, is_wholeprocess):
    """
    统计组内人员预发用例条数
    """
    try:
        FIELPATH = globalparam.file_path
        with open(FIELPATH + '/cases.txt', 'r+') as f:
            old_data = f.read()
            dict_data = json.loads(old_data)
            # 判断是否是是表wholeprocess的全流程性用例，分开存储
            if is_wholeprocess is True:
                end_flag = '_wholeprocess'
            elif is_wholeprocess is False:
                end_flag = '_old'
            # 查找用例对应的人员，在数量上+1
            for key, value in dict_data.items():
                key_split = key.split('_')[0]
                # 判断人员和是否为全流程接口
                if key_split in case_id and end_flag in key:
                    # 如果zyc之后是-，则满足。过滤zyc和zy这种交集情况
                    if case_id.replace('back-' + key_split, '')[0] == '-':
                        # 判断是否是是表wholeprocess的全流程性用例，分开存储
                        dict_data[key_split + end_flag] = value + 1
                        f.seek(0)
                        f.truncate()
                        f.write(json.dumps(dict_data))
                    else:
                        pass
                else:
                    pass
            f.close()
    except Exception as e:
        Log().error('统计预发接口用例数【{}】失败：{}'.format(case_id, e))

def save_pre_case():
    """
    存储预发接口用例数
    """
    try:
        # 查看当天是否为周五，是周五即往下执行
        local_week = datetime.datetime.today().isoweekday()
        local_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        now_time1 = time.strftime('%H:%M', time.localtime(time.time()))
        now_time = now_time1.replace(":", ".")
        # 当天为周五且时间在16-19点之间执行
        if (local_week == 5) and (19 > float(now_time) > 16):
            redis_conn = OperateRedis()
            # 查看当天是否执行过
            old_record = redis_conn.opreate_redis_list('qa_PRE_cases_record', 'select', content='')
            old_record_dict = json.loads(old_record)
            if old_record_dict['add_day'] == local_day and old_record_dict['status'] == 1:
                # 当天存在执行记录，且状态为1跳过
                pass
            else:
                # 查询redis最近一次周五的预发用例数
                old_data = redis_conn.opreate_redis_list('qa_PRE_cases_num', 'select', content='')
                # 获取当前执行txt文件的用例数
                FIELPATH = globalparam.file_path
                with open(FIELPATH + '/cases.txt', 'r+') as f:
                    new_data = f.read()
                    f.close()
                # 新老用例数进行比对，算出新增的用例数
                contrast_data = {}
                for key, value in json.loads(new_data).items():
                    # 判断新-老数量小于0，使用老的数量
                    if value - json.loads(old_data)[key] < 0:
                        new_value = 0
                    else:
                        new_value = value - json.loads(old_data)[key]
                    contrast_data[key] = new_value
                # 最新用例数上传至redis
                dict_new_data = json.loads(new_data)
                add_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                dict_new_data['add_time'] = add_time
                dict_new_data['add_weekend'] = local_week
                str_new_data = json.dumps(dict_new_data)
                redis_conn.opreate_redis_list('qa_PRE_cases_num', 'add', content=str_new_data)
                # 执行记录上传至redis，status为1
                add_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                new_record = {'status': 1, 'add_day': add_day, 'add_time': add_time}
                redis_conn.opreate_redis_list('qa_PRE_cases_record', 'add', content=json.dumps(new_record))
                # 删除本地txt文件
                os.remove(FIELPATH + '/cases.txt')
                # 处理人员数据为{'黄静芳': 'hjf', '周雅': 'zy', ...}
                CASEKEY = globalparam.case_key
                case_zero = {}
                case_result_old = {}
                case_result = {}
                for douhao in CASEKEY.split(','):
                    case_zero[douhao.split('-')[-1]] = 0
                    case_result_old[douhao.split('-')[-1]] = douhao.split('-')[0]
                    case_result[douhao.split('-')[0]] = douhao.split('-')[-1] + '_old,' + douhao.split('-')[-1] + '_wholeprocess'
                # 合并用例数，处理用例数据为{'hjf': '0', 'zy': '0', ...}
                for key, value in contrast_data.items():
                    case_zero[key.split('_')[0]] = value + case_zero[key.split('_')[0]]
                # 总用例数据倒序排序
                case_result = sorted(case_zero.items(), key=lambda x: x[1], reverse=True)
                case_results = {}
                for i in range(len(case_result)):
                    case_results[case_result[i][0]] = case_result[i][1]
                # 处理用例数据为{'韩晓': '20,10', '张砚程': '30,40', ...}
                cases = {}
                for key, value in case_results.items():
                    cases[case_result_old[key]] = str(contrast_data[key + '_old']) + '+' + \
                                                  str(contrast_data[key + '_wholeprocess'])
                # 拼装钉钉消息内容
                content_base = '预发接口用例新增数\n'
                content = ''
                for key, value in cases.items():
                    content += key + '：' + str(value) + '\n'
                contents = content_base + content
                # 发送钉钉消息
                send_msg_pre(contents)
                Log().info('发送预发用例统计消息：\n {}'.format(contents))
    except Exception as e:
        new_record = {'status': 0, 'add_day': add_day, 'add_time': add_time}
        redis_conn.opreate_redis_list('qa_PRE_cases_record', 'add', content=json.dumps(new_record))
        Log().error('取redis的预发用例数【{}】或者取本地文件用例数【{}】失败：{}'.format(old_data, new_data, e))
        raise

def send_msg_pre(msg):
    """
    将执行结果通过钉钉机器人发送，测试模块
    :return:
    """
    TOEKN_3 = globalparam.ding_token_3
    try:
        webhook = "https://oapi.dingtalk.com/robot/send?access_token={0}".format(TOEKN_3)
        xiaoding = DingtalkChatbot(webhook)
        xiaoding.send_text(msg=msg, is_at_all=False)
    except Exception as e:
        Log().error('钉钉通知失败：{}'.format(e))
        raise

if __name__ == "__main__":
    # aa = DealWithTime('{"schemeUuid":"{{mobile}}","ufiId":"{1}","schemeExplainTime":"{{redis.hash.select.zyc_test_hash.zyc}}"}')
    # print(aa)
    # print(DealWithTime('222--{{指定月01日02时03分05秒}}--111--{{指定11月01日}}--'))
    save_pre_case()
