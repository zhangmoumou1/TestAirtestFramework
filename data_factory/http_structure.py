#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: 张砚程
# @@Create Date: 2021-08-3 14:24:14
# @@Modify Date: 2022-08-30 14:24:34
# @@Description: 接口登录
# @@Copyright  91duobaoyu, Inc. All rights reserved.
# *********************************************************#
import json

from public.methods import *
ENV = globalparam.environment


class HttpStructure(object):

    @staticmethod
    def select_login(type):
        """
        选择登录，admin/wechat/保鱼通APP
        """
        user_info = ReadYaml().get_url_user('username_password')
        username = user_info.split(',')[0]
        headers = {
            "content-type": 'application/json; charset=UTF-8',
            'X-Ca-Stage': 'PRE',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        try:
            if type == 'admin':
                url = 'https://gw2.91duobaoyu.com/systembiz/user/userLogin.do'
                data = {
                    "username": username,
                    "password": "ocAUlP3fYbMcAEdE+jJrxw==",
                    "passwordFlag": True,
                    "systemId": 1,
                    "loginPort": 2
                }
                res = requests.post(url=url, headers=headers, data=json.dumps(data))
                text = json.loads(res.text)
                token = text['data']['token']
                Log().info('登录预发环境后台成功，返回token<{}>'.format(token))
                return token
            elif type == 'wetchat':
                token = 'wx-6b8af150-083c-43f9-92d8-2823c9343e81'
                Log().info('登录预发环境微信环境成功，返回token<{}>'.format(token))
                return token
            elif type == 'baoyutong':
                url = 'https://gw2.91duobaoyu.com/managergateway/lichenbiz/v1/outer/ignore/user/loginV2.do'
                data = {"password": 'ocAUlP3fYbMcAEdE+jJrxw\u003d\u003d', "username": username}
                res = requests.post(url=url, headers=headers, data=json.dumps(data))
                text = json.loads(res.text)
                token = text['data']['token']
                Log().info('登录预发环境保鱼通APP成功，返回token<{}>'.format(token))
                return token
            else:
                raise '登录类型有误，请检查书写是否正确'
        except Exception as e:
            Log().error(f'token获取失败，{text}')

    @staticmethod
    def handle_api(key, name):
        """
        调用接口构造数据
        """
        if ENV == 'PRE':
            api_info = ReadYaml().get_factory_http(key, name)
            token = HttpStructure.select_login(api_info['token'])
            headers = {
                "content-type": 'application/json; charset=UTF-8',
                'X-Ca-Stage': 'PRE',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
                'token': token
            }
            try:
                if api_info['way'] in ['get', 'GET']:
                    if api_info['data'] in ['', 'null']:
                        res = requests.get(url=api_info['url'], headers=headers)
                    else:
                        res = requests.get(url=api_info['url'], headers=headers, params=json.dumps(api_info['data']))
                elif api_info['way'] in ['post', 'POST']:
                    if api_info['data'] in ['', 'null']:
                        res = requests.post(url=api_info['url'], headers=headers)
                    else:
                        res = requests.post(url=api_info['url'], headers=headers, data=json.dumps(api_info['data']))
                text = res.text
                Log().info(f'调用接口<{api_info["url"]}>成功，{text}')
            except Exception as e:
                Log().error(f'调用接口<{api_info["url"]}>失败，请检查格式是否正确')

if __name__ == "__main__":
    HttpStructure.handle_api('zhangyancheng', 'http1')