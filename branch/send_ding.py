#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *********************************************************#
# @@Author: zhangmoumou
# @@Create Date: 2022-09-16 22:24:14
# @@Modify Date: 2022-09-16 22:24:34
# @@Description: 发送钉钉消息
# *********************************************************#
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard
from public.log import Log
from branch import globalparam

TOKEN_1 = globalparam.ding_token_1
TOEKN_2 = globalparam.ding_token_2
TOEKN_3 = globalparam.ding_token_3
TOEKN_4 = globalparam.ding_token_4
TOEKN_5 = globalparam.ding_token_5
TOEKN_6 = globalparam.ding_token_6
ENV = globalparam.environment
ERRORFILE = globalparam.error_file

def send_msg(*args):
    """
    将执行结果通过钉钉机器人发送
    :return:
    """
    try:
        env_dict = {
            'PRE': '预发',
            'TEST': '测试',
            'DEV': '开发',
            'RELEASE': '生产'
        }
        # 0条用例，说明执行出错
        if args[0] == 0:
            title = '查看执行日志'
            if args[5] == '保鱼通APP':
                if ENV == 'PRE':
                    url = 'http://192.168.20.10:8080/jenkins/job/z_pre_teardown/allure'
                elif ENV == 'RELEASE':
                    url = 'http://192.168.20.10:8080/jenkins/job/z_teardown/allure'
            elif args[5] == '凡星名片小程序':
                if ENV == 'PRE':
                    url = 'http://192.168.20.10:8080/jenkins/job/z_pre_teardown_fx/allure'
                elif ENV == 'RELEASE':
                    url = 'http://192.168.20.10:8080/jenkins/job/z_teardown_fx/allure'
            with open(ERRORFILE + '/error.txt', 'r+') as f:
                error = f.read()
                f.truncate(0)
            content = '{}环境应用初始化失败【{}】，请检查服务器运行环境是否正常！'.format(env_dict[ENV], error)
        else:
            title = '查看报告详情'
            if args[5] == '保鱼通APP':
                if ENV == 'PRE':
                    url = 'http://192.168.20.10:8080/jenkins/job/z_pre_teardown/allure'
                elif ENV == 'RELEASE':
                    url = 'http://192.168.20.10:8080/jenkins/job/z_teardown/allure'
            elif args[5] == '凡星名片小程序':
                if ENV == 'PRE':
                    url = 'http://192.168.20.10:8080/jenkins/job/z_pre_teardown_fx/allure'
                elif ENV == 'RELEASE':
                    url = 'http://192.168.20.10:8080/jenkins/job/z_teardown_fx/allure'
            content = "项目：{}  \n" \
                      "环境：{}  \n" \
                      "总用例数：{}  \n" \
                      "通过数：{}  \n" \
                      "错误/失败数：{}  \n" \
                      "忽略数：{}  \n" \
                      "耗费时间：{}s  \n" \
                      "账密：admin/123456".format(args[5], env_dict[ENV], args[0], args[1], args[2],
                                              args[3], args[4])
        btns1 = [{"title": title, "actionURL": url}]
        actioncard = ActionCard(title='{}环境执行结果'.format(env_dict[ENV]),
                                 text=content,
                                 btns=btns1
                                 )
        # 有错误消息发到UI告警群，否则发往日常通知群
        if args[2] > 0:
            webhook = "https://oapi.dingtalk.com/robot/send?access_token={0}".format(TOEKN_6)
            webhook1 = "https://oapi.dingtalk.com/robot/send?access_token={0}".format(TOKEN_1)
            xiaoding = DingtalkChatbot(webhook, pc_slide=False)
            xiaoding.send_action_card(actioncard)
            xiaoding1 = DingtalkChatbot(webhook1, pc_slide=False)
            xiaoding1.send_action_card(actioncard)
        else:
            webhook = "https://oapi.dingtalk.com/robot/send?access_token={0}".format(TOKEN_1)
            xiaoding = DingtalkChatbot(webhook, pc_slide=False)
            xiaoding.send_action_card(actioncard)
        Log().info('钉钉通知成功')
    except Exception as e:
        Log().error('钉钉通知失败：{}'.format(e))
        raise

if __name__ == "__main__":
    send_msg(10, 2, 8, 23,78,8)
