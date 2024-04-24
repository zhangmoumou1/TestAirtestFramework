#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @@Software: PyCharm
# @@ScriptName: commom_operation.py
# @@Author: 游昕旭
# @@Create Date: 2023/2/21 11:30 
# @@Modify Date: 2023/2/21 11:30 
# @@Description: 公共操作-分享
# @@Copyright © 91duobaoyu, Inc. All rights reserved.

from airtest.core.api import *
from public.methods import *


class CommonOperation(PocoPackage):
    """
    保鱼通-分享功能
    """

    def wechat_friends_share(self):
        """
        保鱼通-分享功能-点击微信按钮，成功分享到微信好友并返回保鱼通
        """
        try:
            # 分享弹窗中，点击微信好友-点击搜索框
            self.element_click_any("com.fs.diyi:id/tv_wxfriend_share", "android.widget.ImageView")
            # 输入文件传输助手
            text("文件传输助手")
            # 点击文件传输助手-点击分享-点击返回保鱼通
            if self.env == "PRE":
                self.element_click_any("com.tencent.mm:id/kpm", "com.tencent.mm:id/guw", "com.tencent.mm:id/gui")
            else:
                self.element_click_any("com.tencent.mm:id/kpm", "com.tencent.mm:id/guw", "com.tencent.mm:id/gui")
            return "成功分享到微信好友"
        except:
            Log().info("元素不存在")
            raise

    def wechat_moments_share(self):
        """
        保鱼通-分享功能-点击朋友圈，成功分享并返回保鱼通
        """
        try:
            # 点击朋友圈
            self.element_click_any("com.fs.diyi:id/tv_wxcircle_share")
            # 点击输入框
            self.element_click("com.tencent.mm:id/jsy")
            # 输入UI自动化测试分享
            text("UI自动化测试分享")
            # 点击谁可以看-点击私密-点击完成-点击发表
            self.element_click_any("com.tencent.mm:id/jwl", "text=私密", "com.tencent.mm:id/en", "com.tencent.mm:id/en")
            return "成功分享到朋友圈"
        except:
            Log().info("元素不存在")
            raise

    def enterprise_wechat_friends_share(self):
        """
        保鱼通-分享功能-点击企业微信按钮，成功分享到企业微信好友并返回保鱼通
        """
        try:
            # 点击企业微信-点击搜索
            # self.element_click_any("com.fs.diyi:id/tv_enterprisewx_share", "com.tencent.wework:id/l2k")
            # # 输入文件传输助手
            # text("文件传输助手")
            # # 点击文件传输助手-点击发送-点击返回保鱼通
            # self.element_click_any("com.tencent.wework:id/gc7", "com.tencent.wework:id/cja",
            #                        "com.tencent.wework:id/cj8")

            # 存在无网络的情况，跳过直接返回保鱼通
            self.element_click("com.fs.diyi:id/tv_enterprisewx_share")
            sleep(1)
            self.element_click('com.tencent.wework:id/l1u')
            return "成功分发送到企业微信"
        except:
            Log().info("元素不存在")
            # 存在无网络的情况，跳过直接返回保鱼通
            self.element_click('com.tencent.wework:id/l1u')

    def copy_link_share(self):
        # 点击复制链接按钮，复制链接
        try:
            # 点击复制链接
            self.element_click("com.fs.diyi:id/tv_linkurl_share")
        except:
            Log().info("元素不存在")
            raise

    def return_previous_page(self, num=1):
        """
        操作系统按键返回上一页
        :param num 返回次数
        """
        for i in range(num):
            self.element_click("com.android.systemui:id/back")

    def close_page(self, num=1):
        """
        点击x关闭当前页面
        :param num 返回次数
        """
        for i in range(num):
            self.element_click("com.fs.diyi:id/iv_left_btn_right")

    def click_home(self):
        """
        点击进入首页
        """
        try:
            # 点击首页
            self.element_click_any("com.fs.diyi:id/cl_tab_home")
            if self.element_text_any("com.fs.diyi:id/cl_title") == "保鱼通":
                a = "成功到首页"
            else:
                a = "进入首页失败"
                return a
        except:
            Log().info("元素不存在")
            raise

    def get_date_time(self):
        """
        获取当前时间的年、月、日
        """
        today = datetime.datetime.today()
        year, month, day = str(today.year), str(today.month), str(today.day)
        if int(month) < 10:
            month = '0' + str(month)
        if int(day) < 10:
            day = '0' + str(day)
        return {'year': year, 'month': month, 'day': day}

    def get_date_time_no_zero(self):
        """
        获取当前时间的年、月、日
        """
        today = datetime.datetime.today()
        year, month, day = str(today.year), str(today.month), str(today.day)
        return {'year': year, 'month': month, 'day': day}

    def into_member_customer_info(self):
        """
        进入会员客户信息页面
        """
        try:
            # 点击委我的客户-无手机号客户-选择客户
            self.element_click_any("text=我的客户")
            self.picture_click_any("sunshuo", "A测试.png")
        except:
            Log().info("元素不存在")
            raise

if __name__ == "__main__":
    # CommonOperation().wechat_friends_share()
    # CommonOperation().wechat_moments_share()
    # CommonOperation().enterprise_wechat_friends_share()
    CommonOperation().copy_link_share()
