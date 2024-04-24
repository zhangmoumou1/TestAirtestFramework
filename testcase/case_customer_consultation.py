#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @@Software: PyCharm
# @@Author: 张砚程
# @@Create Date: 2023/8/14 21:53
# @@Modify Date: 2023/8/14 21:53
# @@Description: 客户咨询
# @@Copyright © 91duobaoyu, Inc. All rights reserved.

from public.methods import *
logger = Log()
PocoPackage = PocoPackage()
env = globalparam.environment

@allure.epic("保鱼通")
@allure.feature("首页-客户咨询")
@pytest.mark.skipif(env in ['RELEASE'], reason='线上环境不执行')
class TestCustomerConsultationPre(object):
    """
    招募增员-精选好文
    """
    def setup_class(self):
        MysqlStructure.handle_mysql('zhangyancheng', 'sql6')
        PocoPackage.new_start_app()
        logger.info('--------------开始执行用例----------------')

    data1 = [("客户动态\n1客户咨询提醒")]
    @allure.story("进入消息入口-查看右上角消息通知")
    @pytest.mark.parametrize('expect', data1)
    def test_message_notification(self, expect):
        """初始化消息"""
        # 启动保鱼通APP，点击右上角消息通知入口，初始化消息全部已读（为了验证下面发送消息，能成功收到消息），返回首页
        PocoPackage.element_click_any("text=消息", "全部已读")
        CommonOperation().return_previous_page(1)
        """微信公众号发送消息"""
        # 打开微信APP
        PocoPackage.new_start_app_wechat()
        # 点击进入公众号"保鱼淘保"
        PocoPackage.element_click(text="保鱼淘保")
        # 切换到键盘输入
        PocoPackage.element_click_any("com.tencent.mm:id/b5a", "com.tencent.mm:id/b7l")
        # 点击并输入文本
        PocoPackage.element_input("com.tencent.mm:id/kii", input='自动化测试')
        # 点击发送
        PocoPackage.element_click("com.tencent.mm:id/b8k")
        # 切换到语言输入
        PocoPackage.element_click("com.tencent.mm:id/b7l")
        # 长按发送语言
        PocoPackage.element_long_click("com.tencent.mm:id/lbh", duration=10)
        """查看消息"""
        # 启动保鱼通APP
        PocoPackage.new_start_app()
        # 点击右上角消息通知入口
        PocoPackage.element_click(text="消息")
        actual1 = PocoPackage.element_text("客户动态\n1")
        actual2 = PocoPackage.picture_text("\\zhangyancheng\\tpl1691979640674.png")
        new_assert_contains('消息数和消息标题', expect, actual1 + actual2)

    data2 = [('2')]
    @allure.story("查看我的tab和客户咨询入口，角标展示消息数")
    @pytest.mark.parametrize('expect', data2)
    def test_view_message_number(self, expect):
        # 返回到首页
        CommonOperation().return_previous_page(1)
        actual = PocoPackage.element_text("com.fs.diyi:id/tv_new_chat_number")
        new_assert_contains('我的tab和客户咨询入口的消息数', expect, actual)

    data3 = [(["客户咨询", "待处理\n第 1 个标签，共 2 个", "全部\n第 2 个标签，共 2 个"])]
    @allure.story("进入我的tab-客户咨询成功")
    @pytest.mark.parametrize('expect', data3)
    def test_enter_customer_consultation(self, expect):
        # 点击我的tab，点击客户咨询入口
        PocoPackage.element_click_any("com.fs.diyi:id/cl_tab_mine", "text=客户咨询")
        # 获取页面标题，待处理和全部标签名称
        actual = PocoPackage.element_text_any("客户咨询", "待处理\n第 1 个标签，共 2 个", "全部\n第 2 个标签，共 2 个")
        new_assert_contains('页面标题，待处理和全部标签名称', expect, actual)

    data4 = [('欢乐马保鱼选险 [未回复]')]
    @allure.story("客户咨询-待处理列表信息正确")
    @pytest.mark.parametrize('expect', data4)
    def test_pending_list(self, expect):
        # 获取客户昵称、"未回复"、客户最近一条消息内容、标签名"保鱼选险"
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1691981115629.png")
        new_assert_contains('客户昵称、客户最近一条消息内容、标签名', expect, actual)

    data5 = [('欢乐马保鱼选险 [未回复]')]
    @allure.story("客户咨询-全部列表信息正确")
    @pytest.mark.parametrize('expect', data5)
    def test_full_list(self, expect):
        # 点击“全部”列表
        PocoPackage.element_click("全部\n第 2 个标签，共 2 个")
        # 获取客户昵称、"未回复"、客户最近一条消息内容、标签名"保鱼选险"
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1691981115629.png")
        new_assert_contains('客户昵称、客户最近一条消息内容、标签名', expect, actual)

    data6 = [("欢乐马自动化测试")]
    @allure.story("客户咨询-进入对话页面成功")
    @pytest.mark.parametrize('expect', data6)
    def test_enter_chat_page(self, expect):
        # 点击昵称进入对话页面
        PocoPackage.picture_click("\\zhangyancheng\\tpl1691982296885.png")
        # 获取页面标题和对话内容
        actual1 = PocoPackage.element_text_any("欢乐马")
        actual2 = PocoPackage.picture_text("\\zhangyancheng\\tpl1692321391633.png")
        new_assert_contains('页面标题', expect, actual1 + actual2)

    data7 = [("收到谢谢")]
    @allure.story("客户咨询-对话页面-发送文本成功")
    @pytest.mark.parametrize('expect', data7)
    def test_chat_page_send_message(self, expect):
        # 点击输入框，输入文本，发送
        PocoPackage.element_input("android.widget.EditText", input="收到谢谢", enter=True)
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1691984591450.png")
        new_assert_contains('已发送的文本', expect, actual)

    data8 = [(["图片", "名片"])]
    @allure.story("客户咨询-对话页面-打开更多操作成功")
    @pytest.mark.parametrize('expect', data8)
    def test_more_functions(self, expect):
        # 点击输入框后的加号按钮
        PocoPackage.picture_click("\\zhangyancheng\\tpl1691984818037.png")
        actual = PocoPackage.element_text_any("图片", "名片")
        new_assert_contains('弹窗图片和名片名称', expect, actual)

    data9 = [('打开图片')]
    @allure.story("客户咨询-对话页面-发送图片成功")
    @pytest.mark.parametrize('expect', data9)
    def test_send_picture(self, expect):
        # 选择图片
        PocoPackage.element_click("图片")
        # 判断访问文件权限
        if PocoPackage.element_text('com.lbe.security.miui:id/permission_applicant') == '要允许 保鱼通 访问以下权限吗？':
            PocoPackage.element_click('android:id/button1')
        PocoPackage.element_click_any("显示根目录", "text=相册", "text=相册", "text=自动化",
                                      "com.miui.gallery:id/micro_thumb")
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1692083526914.png")
        # 发送图片后，回到app可能会出现socket断开，需要重连。再次发送图片
        # if PocoPackage.element_text("网络连接中断，是否要重新连接？") == '网络连接中断，是否要重新连接？':
        #     PocoPackage.element_click("再次连接")
        #     PocoPackage.element_click_any("图片", "显示根目录", "text=相册", "text=相册", "text=自动化",
        #                                   "com.miui.gallery:id/micro_thumb")
        # 如果点击重连无反应，则取消
        if PocoPackage.element_text("网络连接中断，是否要重新连接？") == '网络连接中断，是否要重新连接？':
            PocoPackage.element_click("取消")
            # PocoPackage.element_click_any("图片", "显示根目录", "text=相册", "text=相册", "text=自动化",
            #                               "com.miui.gallery:id/micro_thumb")
        new_assert_contains('发送图片的内容', expect, actual)

    data10 = [('未发送名片')]
    @allure.story("客户咨询-对话页面-取消发送名片成功")
    @pytest.mark.parametrize('expect', data10)
    def test_send_card_cancel(self, expect):
        # 点击名片、点击取消发送
        PocoPackage.element_click_any("名片", "取消")
        text = PocoPackage.picture_text("\\zhangyancheng\\tpl1692085961158.png")
        if text is False:
            actual = '未发送名片'
        new_assert_contains('发送图片的内容', expect, actual)

    data11 = [('员工名片')]
    @allure.story("客户咨询-对话页面-发送名片成功")
    @pytest.mark.parametrize('expect', data11)
    def test_send_card(self, expect):
        if PocoPackage.element_text("网络连接中断，是否要重新连接？") == "网络连接中断，是否要重新连接？":
            PocoPackage.element_click("再次连接")
        PocoPackage.element_click_any("名片", "发送")
        if PocoPackage.element_text("网络连接中断，是否要重新连接？") == "网络连接中断，是否要重新连接？":
            PocoPackage.element_click("再次连接")
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1692085961158.png")
        new_assert_contains('发送名片内容', expect, actual)

    data12 = [('所在地"浙江省-杭州市"\n保鱼选险')]
    @allure.story("客户咨询-对话页面-标签展示正确")
    @pytest.mark.parametrize('expect', data12)
    def test_tag(self, expect):
        actual = PocoPackage.element_text('所在地"浙江省-杭州市"\n保鱼选险')
        new_assert_contains('标签内容', expect, actual)

    data13 = [('复制')]
    @allure.story("客户咨询-对话页面-长按文本弹出复制操作")
    @pytest.mark.parametrize('expect', data13)
    def test_longclick_text(self, expect):
        # 长按文本"收到谢谢"
        PocoPackage.picture_swipe("\\zhangyancheng\\tpl1692169057671.png", record_pos=(0.222, -0.543),
                                  resolution=(1080, 2340), vector=[0.0002, 0.0012], duration=3)
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1692168852980.png")
        new_assert_contains('复制按钮文本', expect, actual)

    data14 = [('复制成功')]
    @allure.story("客户咨询-对话页面-复制文本成功")
    @pytest.mark.parametrize('expect', data14)
    def test_copy_text(self, expect):
        # 点击复制
        PocoPackage.picture_click("\\zhangyancheng\\tpl1692168852980.png")
        actual = PocoPackage.ocr_text("复制文本消息成功", locate=(140, 360, 230, 395))
        new_assert_contains('复制文本消息toast', expect, actual)

    data15 = [('听简播放')]
    @allure.story("客户咨询-对话页面-长按语音切换至听筒播放方式")
    @pytest.mark.parametrize('expect', data15)
    def test_longclick_voice_1(self, expect):
        # 长按语音消息
        PocoPackage.picture_swipe("\\zhangyancheng\\tpl1692170010136.png", record_pos=(-0.284, -0.736),
                                  resolution=(1080, 2340), vector=[0.0052, 0.0009], duration=3)
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1692170167117.png")
        new_assert_contains('切换听筒方式的文本', expect, actual)

    data16 = [('切换成功')]
    @allure.story("客户咨询-对话页面-语音切换到听筒方式成功")
    @pytest.mark.parametrize('expect', data16)
    def test_switchover_telephone_receiver(self, expect):
        # 点击切换到听筒播放
        PocoPackage.picture_click("\\zhangyancheng\\tpl1692170167117.png")
        actual = PocoPackage.ocr_text("复制文本消息成功", locate=(140, 360, 230, 395))
        new_assert_contains('切换到听筒成功toast', expect, actual)

    data17 = [('切换成功')]
    @allure.story("客户咨询-对话页面-语音切换到扬声器方式成功")
    @pytest.mark.parametrize('expect', data17)
    def test_switchover_loudspeaker(self, expect):
        # 长按语音消息
        PocoPackage.picture_swipe("\\zhangyancheng\\tpl1692170010136.png", record_pos=(-0.284, -0.736),
                                  resolution=(1080, 2340), vector=[0.0052, 0.0009], duration=3)
        # 点击切换到扬声器播放
        PocoPackage.picture_click("\\zhangyancheng\\tpl1692171017428.png")
        actual = PocoPackage.ocr_text("复制文本消息成功", locate=(140, 360, 230, 395))
        new_assert_contains('切换到扬声器成功toast', expect, actual)

    data18 = [('')]
    @allure.story("客户咨询-对话页面-点击播放语音")
    @pytest.mark.parametrize('expect', data18)
    def test_play_voice(self, expect):
        # 点击语音文案播放
        PocoPackage.picture_click("\\zhangyancheng\\tpl1692171820349.png")
        # 无法识别播放成功，能定位到即可
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1692171763793.png")
        new_assert_contains('播放成功的标记', expect, actual)

    data19 = [('保存图片')]
    @allure.story("客户咨询-对话页面-点击打开图片")
    @pytest.mark.parametrize('expect', data19)
    def test_open_picture(self, expect):
        # 点击图片
        PocoPackage.picture_click("\\zhangyancheng\\tpl1692083526914.png")
        actual = PocoPackage.element_text("保存图片")
        new_assert_contains('保存图片按钮文本', expect, actual)

    # data20 = [('下载完成')]
    # @allure.story("客户咨询-对话页面-保存图片成功")
    # @pytest.mark.parametrize('expect', data20)
    # def test_save_picture(self, expect):
    #     # 点击图片
    #     PocoPackage.element_click("保存图片")
    #     actual = PocoPackage.ocr_text_continue('下载完成', "下载图片成功", locate=(120, 380, 250, 405))
    #     new_assert_contains('图片保存成功的toast', expect, actual)

    data21 = [('收到谢谢')]
    @allure.story("客户咨询-对话页面-点击关闭图片")
    @pytest.mark.parametrize('expect', data21)
    def test_close_picture(self, expect):
        # 点击图片
        PocoPackage.picture_click("\\zhangyancheng\\tpl1692083526914.png")
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1691984591450.png")
        new_assert_contains('对话框回复的文本', expect, actual)

    data22 = [(["是否接客", "是否休息"])]
    @allure.story("客户咨询-进入设置页")
    @pytest.mark.parametrize('expect', data22)
    def test_enter_settings(self, expect):
        # 返回上一页
        CommonOperation().return_previous_page(1)
        # 点击"设置"按钮
        PocoPackage.element_click("设置")
        actual = PocoPackage.element_text_any("是否接客", "是否休息")
        new_assert_contains('按钮名称', expect, actual)

    data23 = [('已全部关闭')]
    @allure.story("客户咨询-设置页-关闭接口和休息按钮")
    @pytest.mark.parametrize('expect', data23)
    def test_close_settings(self, expect):
        # 关闭是否接口和是否休息按钮
        PocoPackage.element_click_any("是否接客", "是否休息")
        # 获取关闭按钮样式结果，存在会返回空字符串，不存在会返回Flase
        text1 = PocoPackage.picture_text("\\zhangyancheng\\tpl1692235453899.png", timeout=3)
        # 获取开启按钮样式结果，存在会返回空字符串，不存在会返回Flase
        text2 = PocoPackage.picture_text("\\zhangyancheng\\tpl1692235848090.png", timeout=3)
        if (text1 is not False) and text2 is False:
            actual = '已全部关闭'
        else:
            actual = '未全部关闭'
        new_assert_contains('按钮样式', expect, actual)

    data24 = [('已全部打开')]
    @allure.story("客户咨询-设置页-开启接口和休息按钮")
    @pytest.mark.parametrize('expect', data24)
    def test_open_settings(self, expect):
        # 关闭是否接口和是否休息按钮
        PocoPackage.element_click_any("是否接客", "是否休息")
        # 获取关闭按钮样式结果，存在会返回空字符串，不存在会返回Flase
        text1 = PocoPackage.picture_text("\\zhangyancheng\\tpl1692235453899.png", timeout=3)
        # 获取开启按钮样式结果，存在会返回空字符串，不存在会返回Flase
        text2 = PocoPackage.picture_text("\\zhangyancheng\\tpl1692235848090.png", timeout=3)
        if (text1 is False) and (text2 is not False):
            actual = '已全部打开'
        else:
            actual = '未全部打开'
        new_assert_contains('按钮样式', expect, actual)

    data25 = [(['客户咨询', '待处理\n第 1 个标签，共 2 个', '全部\n第 2 个标签，共 2 个'])]
    @allure.story("从首页进入客户咨询页")
    @pytest.mark.parametrize('expect', data25)
    def test_home_to_customer_consultation(self, expect):
        # 返回我的页面，点击首页
        CommonOperation().return_previous_page(2)
        PocoPackage.element_click("com.fs.diyi:id/cl_tab_home")
        # 点击客户咨询入口
        PocoPackage.element_click(text="客户咨询")
        # 获取页面标题，待处理和全部标签名称
        actual = PocoPackage.element_text_any("客户咨询", "待处理\n第 1 个标签，共 2 个", "全部\n第 2 个标签，共 2 个")
        new_assert_contains('页面标题，待处理和全部标签名称', expect, actual)

    def teardown_class(self):
        PocoPackage.new_stop_app()
        Log().info('----------------用例执行完成-----------------')


@allure.epic("保鱼通")
@allure.feature("首页-客户咨询")
@pytest.mark.skipif(env in ['PRE'], reason='预发环境不执行')
class TestCustomerConsultationRelease(object):
    """
    首页-客户咨询
    """
    def setup_class(self):
        PocoPackage.new_start_app()
        logger.info('--------------开始执行用例----------------')

    data1 = [(["客户咨询", "待处理\n第 1 个标签，共 2 个", "全部\n第 2 个标签，共 2 个"])]

    @allure.story("进入我的tab-客户咨询成功")
    @pytest.mark.parametrize('expect', data1)
    def test_enter_customer_consultation(self, expect):
        # 点击我的tab，点击客户咨询入口
        PocoPackage.element_click_any("com.fs.diyi:id/cl_tab_mine", "text=客户咨询")
        # 获取页面标题，待处理和全部标签名称
        actual = PocoPackage.element_text_any("客户咨询", "待处理\n第 1 个标签，共 2 个", "全部\n第 2 个标签，共 2 个")
        new_assert_contains('页面标题，待处理和全部标签名称', expect, actual)

    data2 = [('')]
    @allure.story("客户咨询-切换至全部列表成功")
    @pytest.mark.parametrize('expect', data2)
    def test_full_list(self, expect):
        # 点击“全部”列表
        PocoPackage.element_click("全部\n第 2 个标签，共 2 个")
        # 能定位到，文字颜色问题无法识别
        actual = PocoPackage.picture_text("\\zhangyancheng\\tpl1692250954945.png")
        new_assert_contains('无消息文案', expect, actual)

    data3 = [(["是否接客", "是否休息"])]
    @allure.story("客户咨询-进入设置页")
    @pytest.mark.parametrize('expect', data3)
    def test_enter_settings(self, expect):
        # 点击"设置"按钮
        PocoPackage.element_click("设置")
        actual = PocoPackage.element_text_any("是否接客", "是否休息")
        new_assert_contains('按钮名称', expect, actual)

    data4 = [('已全部关闭')]
    @allure.story("客户咨询-设置页-关闭接口和休息按钮")
    @pytest.mark.parametrize('expect', data4)
    def test_close_settings(self, expect):
        # 关闭是否接口和是否休息按钮
        PocoPackage.element_click_any("是否接客", "是否休息")
        # 获取关闭按钮样式结果，存在会返回空字符串，不存在会返回Flase
        text1 = PocoPackage.picture_text("\\zhangyancheng\\tpl1692235453899.png", timeout=3)
        # 获取开启按钮样式结果，存在会返回空字符串，不存在会返回Flase
        text2 = PocoPackage.picture_text("\\zhangyancheng\\tpl1692235848090.png", timeout=3)
        if (text1 is not False) and text2 is False:
            actual = '已全部关闭'
        else:
            actual = '未全部关闭'
        new_assert_contains('按钮样式', expect, actual)

    data5 = [('已全部打开')]
    @allure.story("客户咨询-设置页-开启接口和休息按钮")
    @pytest.mark.parametrize('expect', data5)
    def test_open_settings(self, expect):
        # 关闭是否接口和是否休息按钮
        PocoPackage.element_click_any("是否接客", "是否休息")
        # 获取关闭按钮样式结果，存在会返回空字符串，不存在会返回Flase
        text1 = PocoPackage.picture_text("\\zhangyancheng\\tpl1692235453899.png", timeout=3)
        # 获取开启按钮样式结果，存在会返回空字符串，不存在会返回Flase
        text2 = PocoPackage.picture_text("\\zhangyancheng\\tpl1692235848090.png", timeout=3)
        if (text1 is False) and (text2 is not False):
            actual = '已全部打开'
        else:
            actual = '未全部打开'
        new_assert_contains('按钮样式', expect, actual)

    data6 = [(['客户咨询', '待处理\n第 1 个标签，共 2 个', '全部\n第 2 个标签，共 2 个'])]
    @allure.story("从首页进入客户咨询页")
    @pytest.mark.parametrize('expect', data6)
    def test_home_to_customer_consultation(self, expect):
        # 返回我的页面，点击首页
        CommonOperation().return_previous_page(2)
        PocoPackage.element_click("com.fs.diyi:id/cl_tab_home")
        # 点击客户咨询入口
        PocoPackage.element_click(text="客户咨询")
        # 获取页面标题，待处理和全部标签名称
        actual = PocoPackage.element_text_any("客户咨询", "待处理\n第 1 个标签，共 2 个", "全部\n第 2 个标签，共 2 个")
        new_assert_contains('页面标题，待处理和全部标签名称', expect, actual)

    def teardown_class(self):
        PocoPackage.new_stop_app()
        Log().info('----------------用例执行完成-----------------')

"""
数据
1、res_dispatch.distribute_record表，用户user_id=1021080500018393和empId=315存在关系才会收到消息
2、客户昵称：欢乐马，
3、标签：保鱼选险

"""