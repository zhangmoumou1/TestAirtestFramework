#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @@ScriptName: case_my_performance.py
# @@Author: 霍寒、张砚程
# @@Create Date: 2023/5/01 10:44
# @@Modify Date: 2023/5/01 10:44
# @@Description: 保鱼通-我的—我的业绩：业绩概览、工资单
# @@Copyright © 91duobaoyu, Inc. All rights reserved.

from public.methods import *
logger = Log()
PocoPackage = PocoPackage()
env = globalparam.environment


@allure.epic("保鱼通")
@allure.feature("我的-我的业绩-业绩概览")
@pytest.mark.skipif(env in ['RELEASE'], reason='线上环境不执行')
class TestMyPerformance(object):
    """
    保鱼通-我的—我的业绩-业绩概览
    """
    # 获取当前年、月、日
    locate = CommonOperation().get_date_time()['year'] + '-' + CommonOperation().get_date_time()['month'] + '-' + \
             CommonOperation().get_date_time()['day']
    def setup_class(self):
        # 执行sql展示本月业绩数据
        MysqlStructure.handle_mysql('zhangyancheng', 'sql4')
        PocoPackage.new_start_app()
        logger.info('--------------开始执行用例----------------')

    data1 = [("39.00")]
    @allure.story("切换到我的tab页-查看本月业绩")
    @pytest.mark.parametrize('expect', data1)
    def test_performance_mine_page(self, expect):
        """
        进入我的页面，查看本月业绩
        """
        # 点击"首页"tab、"我的"tab
        PocoPackage.element_click_any("com.fs.diyi:id/cl_tab_home", "com.fs.diyi:id/cl_tab_mine")
        actual = PocoPackage.element_text("com.fs.diyi:id/tv_achievement")
        new_assert_contains('我的tab页面本月业绩金额', expect, actual)

    data2 = [(f"¥ 39.00保单号：zhangyc00010\n¥ 1.00\n{locate}\n已退保")]
    @allure.story("我的-我的业绩-进入业绩概览页面成功")
    @pytest.mark.parametrize('expect', data2)
    def test_performance_enter_page(self, expect):
        # 点击“查看更多”入口
        PocoPackage.element_click("com.fs.diyi:id/tv_mine_achievement_detail")
        actual1 = PocoPackage.element_text("¥ 39.00")
        actual2 = PocoPackage.element_text(f"保单号：zhangyc00010\n¥ 1.00\n{TestMyPerformance.locate}\n已退保")
        new_assert_contains('首年佣金、已退保保单全部信息', expect, actual1 + actual2)

    data3 = [("保单号：zhangyc0006\n¥ 6.00\n")]
    @allure.story("我的-我的业绩-业绩概览列表滑动成功")
    @pytest.mark.parametrize('expect', data3)
    def test_performance_overview_swipe(self, expect):
        # 滑动至底部
        PocoPackage.element_swipe(f"保单号：zhangyc0002\n¥ 2.00\n{TestMyPerformance.locate}", swipe=[0.0806, -0.4753])
        actual = PocoPackage.element_text(f"保单号：zhangyc0006\n¥ 6.00\n{TestMyPerformance.locate}")
        new_assert_contains('列表最末尾保单的全部信息', expect, actual)

    data4 = [('否')]
    @allure.story("我的-我的业绩-业绩概览进入保单详情成功")
    @pytest.mark.parametrize('expect', data4)
    def test_performance_overview_enter_policy_detail(self, expect):
        # 点击保单
        PocoPackage.element_click(f"保单号：zhangyc0006\n¥ 6.00\n{TestMyPerformance.locate}")
        actual = PocoPackage.element_text(text="否", timeout=12)
        new_assert_contains('基本信息的退保状态', expect, actual)

    data5 = [(['医疗险', '100元'])]
    @allure.story("我的-我的业绩-业绩概览-保单详情-切换至保障内容tab页成功")
    @pytest.mark.parametrize('expect', data5)
    def test_performance_overview_policy_safeguard(self, expect):
        # 点击切换至保障内容tab页
        PocoPackage.picture_click("\\zhangyancheng\\tpl1686193880613.png")
        actual = PocoPackage.element_text_any("text=医疗险", "text=100元")
        new_assert_contains('险种、保费', expect, actual)

    data6 = [(['15868167653', '系统保单'])]
    @allure.story("我的-我的业绩-业绩概览-保单详情-切换至客户信息tab页成功")
    @pytest.mark.parametrize('expect', data6)
    def test_performance_overview_policy_userinfo(self, expect):
        # 点击切换至客户信息tab页
        PocoPackage.picture_click("\\zhangyancheng\\tpl1686193930058.png")
        actual = PocoPackage.element_text_any("text=15868167653", "text=系统保单")
        new_assert_contains('投保人手机号码、被保人姓名', expect, actual)

    data7 = [('100%')]
    @allure.story("我的-我的业绩-业绩概览-保单详情-滑动客户信息至底部成功")
    @pytest.mark.parametrize('expect', data7)
    def test_performance_overview_policy_swipe(self, expect):
        # 滑动客户信息至底部成功
        PocoPackage.element_swipe(text="系统保单", swipe=[0.1075, -0.3513])
        actual = PocoPackage.element_text(text="100%")
        new_assert_contains('受益人信息的收益比例', expect, actual)

    data8 = [('日期选择')]
    @allure.story("我的-我的业绩-业绩概览-点击日期切换成功弹窗")
    @pytest.mark.parametrize('expect', data8)
    def test_performance_overview_datetime(self, expect):
        # 返回上一页
        CommonOperation().return_previous_page(1)
        # 获取当前年、月
        locate = CommonOperation().get_date_time()['year'] + '.' + CommonOperation().get_date_time()['month']
        # 点击右上角日期
        PocoPackage.element_click(locate)
        actual = PocoPackage.element_text("日期选择")
        new_assert_contains('日期选择弹窗的标题', expect, actual)

    data9 = [(['2022.01', '¥ 0.00'])]
    @allure.story("我的-我的业绩-业绩概览-日期选择2022年成功/无佣金展示")
    @pytest.mark.parametrize('expect', data9)
    def test_performance_overview_select_datetime(self, expect):
        # 获取当前年
        year = CommonOperation().get_date_time()['year'] + '年'
        # 滑动到上一年
        PocoPackage.element_swipe(year, swipe=[0.0179, 0.062])
        # 点击确定
        PocoPackage.element_click("确定")
        actual = PocoPackage.element_text_any("2022.01", "¥ 0.00")
        new_assert_contains('选择后的2022.01日期、佣金金额', expect, actual)

    def teardown_class(self):
        # 返回上一页
        PocoPackage.new_stop_app()
        Log().info('----------------用例执行完成-----------------')


@allure.epic("保鱼通")
@allure.feature("我的-我的业绩-工资单")
@pytest.mark.skipif(env in ['RELEASE'], reason='线上环境不执行')
class TestMyPay(object):
    """
    保鱼通-我的—我的业绩-工资单
    """

    def setup_class(self):
        PocoPackage.new_start_app()
        logger.info('--------------开始执行用例----------------')

    data1 = [(["1月","税后实发工资","首年佣金","业绩奖金","续期佣金","增员奖金","销售总监管理津贴","营销合伙人区域管理津贴","销售合伙人区域管理津贴"])]
    @allure.story("进入我的-我的业绩-工资单加载成功")
    @pytest.mark.parametrize('expect', data1)
    def test_enter_my_pay(self, expect):
        # 获取当前月份
        locate = CommonOperation().get_date_time()['month']
        # 点击"我的"tab、我的业绩
        PocoPackage.element_click_any("com.fs.diyi:id/cl_tab_mine", "com.fs.diyi:id/tv_mine_achievement_detail")
        #点击工资单
        PocoPackage.picture_click("\\huohan\\tpl1685602446838.png")
        #点击右上角月份
        PocoPackage.element_click_any("2023." + locate)
        #将月份切换到1月
        PocoPackage.element_swipe(CommonOperation().get_date_time_no_zero()['month'] + '月', swipe=[0.0204, 0.4369])
        PocoPackage.element_click_any("确定")
        #检查工资单数据显示
        actual = PocoPackage.element_text_any("1月","税后实发工资","首年佣金","业绩奖金","续期佣金","增员奖金","销售总监管理津贴","营销合伙人区域管理津贴","销售合伙人区域管理津贴")
        new_assert_contains('4月工资单初始页面', expect, actual)

    data2 = [("2023.01")]
    @allure.story("工资单月份切换到1月，1月回显成功")
    @pytest.mark.parametrize('expect', data2)
    def test_my_pay001(self, expect):
        #检查右上角月份显示
        actual = PocoPackage.element_text_any("2023.01")
        new_assert_contains('工资单月份切换到1月，1月回显成功', expect, actual)

    data3 =[(["¥ 12999","122","125","129"])]
    @allure.story("实发工资、佣金值、津贴值正常显示")
    @pytest.mark.parametrize('expect', data3)
    def test_my_pay002(self, expect):
        #实发工资、佣金值、津贴值显示
        actual = PocoPackage.element_text_any("¥ 12999","122","125","129")
        new_assert_contains('实发工资、佣金值、津贴值正常显示', expect, actual)

    data4 = [("查看详细明细")]
    @allure.story("下滑工资单页面,查看详细明细按钮显示")
    @pytest.mark.parametrize('expect', data4)
    def test_my_pay003(self, expect):
        PocoPackage.element_swipe("销售合伙人区域管理津贴", swipe=[-0.0529, -0.6722])
        #下滑工资单页面查看详细明细按钮显示
        actual = PocoPackage.element_text_any("查看详细明细")
        new_assert_contains('下滑工资单页面,查看详细明细按钮显示', expect, actual)

    data5 = [(["团队续期","总监育成津贴","加佣","团财佣金","宣传推广奖励","其他","应发月薪总计","个人所得税","税后实发工资"])]
    @allure.story("下滑工资单页面，第二页字段名称加载正常")
    @pytest.mark.parametrize('expect', data5)
    def test_my_pay004(self, expect):
        #获取第二页工资单字段名称
        actual = PocoPackage.element_text_any("团队续期","总监育成津贴","加佣","团财佣金","宣传推广奖励","其他","应发月薪总计","个人所得税","税后实发工资")
        new_assert_contains('下滑工资单页面，第二页字段名称加载正常', expect, actual)

    data6 =[(["130","132","134","136","12999"])]
    @allure.story("第二页的实发工资、佣金值、津贴值正常显示")
    @pytest.mark.parametrize('expect', data6)
    def test_my_pay005(self, expect):
        #第二页的工资单实发工资、佣金值、津贴值正常显示
        actual = PocoPackage.element_text_any("130","132","134","136","12999")
        new_assert_contains('第二页的实发工资、佣金值、津贴值正常显示', expect, actual)

    data7 =[(["保单号: baodanhao001","产品名称: 妈咪宝贝","保费: 1986","2023-03-01","佣金: 198.6"])]
    @allure.story("工资单页面下滑至底部，点击产品详情明细按钮，检查首年佣金详情显示")
    @pytest.mark.parametrize('expect', data7)
    def test_my_pay006(self, expect):
        #点击查看详细明细按钮
        PocoPackage.element_click_any("查看详细明细")
        #获取首年佣金的保单号、产品名称、保费、下单时间、佣金
        actual = PocoPackage.picture_text_any("huohan","tpl1685611182918.png","tpl1685611192904.png","tpl1685611206648.png","tpl1685611277373.png","tpl1685611285401.png")
        new_assert_contains('工资单页面下滑至底部，点击产品详情明细按钮，检查首年佣金详情显示', expect, actual)

    data8 =[(["保单号: baodanhao020","产品名称: 妈咪宝贝","保费: 2005","2023-03-20","佣金: 198.25"])]
    @allure.story("首年佣金详情下滑至最后一条数据，查看数据展示")
    @pytest.mark.parametrize('expect', data8)
    def test_my_pay007(self, expect):
        #首年佣金详情下滑至最后一条数据
        PocoPackage.picture_swipe("\\huohan\\tpl1685670891782.png", record_pos=(-0.232, 0.355),
                                  resolution=(1080, 2280), vector=[0.074, -0.3809])
        PocoPackage.picture_swipe("\\huohan\\tpl1685671312880.png", record_pos=(-0.231, 0.701),
                                  resolution=(1080, 2280), vector=[-0.0136, -0.6474])
        PocoPackage.picture_swipe("\\huohan\\tpl1685671460141.png", record_pos=(-0.231, 0.701),
                                  resolution=(1080, 2280), vector=[-0.0136, -0.6474])
        PocoPackage.picture_swipe("\\huohan\\tpl1685671519241.png", record_pos=(-0.231, 0.701),
                                  resolution=(1080, 2280), vector=[-0.0136, -0.6474])
        PocoPackage.picture_swipe("\\huohan\\tpl1685671565355.png", record_pos=(-0.231, 0.701),
                                  resolution=(1080, 2280), vector=[-0.0136, -0.6474])
        PocoPackage.picture_swipe("\\huohan\\tpl1685671610952.png", record_pos=(-0.231, 0.701),
                                  resolution=(1080, 2280), vector=[-0.0136, -0.6474])
        PocoPackage.picture_swipe("\\huohan\\tpl1685671646740.png", record_pos=(-0.231, 0.701),
                                  resolution=(1080, 2280), vector=[-0.0136, -0.6474])
        PocoPackage.picture_swipe("\\huohan\\tpl1685671690003.png", record_pos=(-0.231, 0.701),
                                  resolution=(1080, 2280), vector=[-0.0136, -0.6474])
        PocoPackage.picture_swipe("\\huohan\\tpl1685671722177.png", record_pos=(-0.231, 0.701),
                                  resolution=(1080, 2280), vector=[-0.0136, -0.6474])
        #获取最后一条首年佣金的保单号、产品名称、保费、下单时间、佣金
        actual = PocoPackage.picture_text_any("huohan","tpl1685672570804.png","tpl1685672579361.png","tpl1685672586604.png","tpl1685672592586.png","tpl1685672597120.png")
        new_assert_contains('首年佣金详情下滑至最后一条数据，查看数据展示', expect, actual)

    data9 =[(["保单号: xvqibaodanhao001","产品名称: 某续期产品","保费: 1998","2023-03-01","佣金: 200"])]
    @allure.story("从首年佣金切换到续期佣金，检查续期佣金的保单号、产品名称、保费、下单时间、佣金显示")
    @pytest.mark.parametrize('expect', data9)
    def test_my_pay008(self, expect):
        #从首年佣金切换到续期佣金
        PocoPackage.picture_click("\\huohan\\tpl1685673486413.png")
        #获取续期佣金的保单号、产品名称、保费、下单时间、佣金
        actual = PocoPackage.picture_text_any("huohan","tpl1685673545668.png","tpl1685673552588.png","tpl1685673575205.png","tpl1685673580500.png","tpl1685673584235.png")
        new_assert_contains('从首年佣金切换到续期佣金，检查续期佣金的保单号、产品名称、保费、下单时间、佣金显示', expect, actual)

    data10 = [(["加佣: 366.78", "加佣方案: 加佣方案1", "备注说明: 备注说明1"])]
    @allure.story("从续期佣金切换到加佣，检查加佣、加佣方案、备注说明显示")
    @pytest.mark.parametrize('expect', data10)
    def test_my_pay009(self, expect):
        # 从续期佣金切换到加佣
        PocoPackage.picture_click("\\huohan\\tpl1685673882090.png")
        # 获取加佣、加佣方案、备注说明显示
        actual = PocoPackage.picture_text_any("huohan", "tpl1685673897123.png", "tpl1685673902737.png",
                                              "tpl1685673907066.png")
        new_assert_contains('从续期佣金切换到加佣，检查加佣、加佣方案、备注说明显示', expect, actual)

    data11 = [(["其他: 234.01", "备注说明: 备注说明1"])]
    @allure.story("从加佣切换到其他，检查其他的佣金、备注说明显示")
    @pytest.mark.parametrize('expect', data11)
    def test_my_pay010(self, expect):
        # 从加佣切换到其他
        PocoPackage.picture_click("\\huohan\\tpl1685673915125.png")
        # 获取其他的佣金、备注说明显示
        actual = PocoPackage.picture_text_any("huohan", "tpl1685673924323.png", "tpl1685673930876.png")
        new_assert_contains('从加佣切换到其他，检查其他的佣金、备注说明显示', expect, actual)

    data12 =(["UI自动化账号（顾问微信gw5945）"])
    @allure.story("从其他点击返回再返回至我的页面")
    @pytest.mark.parametrize('expect', data12)
    def test_my_pay011(self, expect):
        #从其他点击返回再返回至我的页面
        PocoPackage.return_previous_page(2)
        # 获取我的页面的顾问姓名
        actual = PocoPackage.element_text_any("com.fs.diyi:id/tv_name")
        new_assert_contains('从其他点击返回再返回至我的页面', expect, actual)


    def teardown_class(self):
      PocoPackage.new_stop_app()
      Log().info('----------------用例执行完成-----------------')