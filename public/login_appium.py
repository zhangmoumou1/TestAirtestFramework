import pytest
from public.common import CommonPage
from public.log import Log

logger = Log()

class Login(CommonPage):
    """
    保鱼通登录
    :return:
    """
    # 定位器
    login_use_info_loc = ("id", "com.fs.diyi:id/tv_btn_right")
    login_switch_loc = ("id", "com.fs.diyi:id/tv_switch_login_mode")
    login_username_loc = ("id", "com.fs.diyi:id/et_input_account")
    login_password_loc = ("id", "com.fs.diyi:id/et_input_pwd")
    login_agree_loc = ("id", "com.fs.diyi:id/iv_btn_checked")
    login_button_loc = ("id", "com.fs.diyi:id/tv_btn_login")

    # 其他定位
    next_loc = ("id", "com.fs.diyi:id/tv_confirm")
    next_2_loc = ("id", "com.fs.diyi:id/tv_confirm2")
    next_3_loc = ("id", "com.fs.diyi:id/tv_confirm3")
    next_4_loc = ("id", "com.fs.diyi:id/tv_product_desc")

    # 关闭操作
    product_loc = ("xpath", "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ImageView")
    product_1_loc = ("xpath", "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[1]")

    # action
    def login_base(self):
        """
        登录前置操作
        """
        # 同意使用须知
        self.click(self.login_use_info_loc)
        # 切换至工号登录
        self.click(self.login_switch_loc)
        # 同意协议
        self.click(self.login_agree_loc)

    def login_action(self, user_name, password):
        # 输入账密
        self.clear_type(self.login_username_loc, user_name)
        self.clear_type(self.login_password_loc, password)
        # 点击登录
        self.click(self.login_button_loc)

    def login_username_password_error(self, expect):
        """
        账号不存在；密码错误，剩余xx次机会
        :return:
        """
        login_error_loc = ("id", "com.fs.diyi:id/tv_error")
        actual = self.is_text_in_element(login_error_loc, expect)
        return actual

    def login_success(self, expect):
        """
        登录成功
        :return:
        """
        login_success_loc = ("id", "com.fs.diyi:id/tv_confirm")
        actual = self.is_text_in_element(login_success_loc, expect)
        return actual

    def driver_quit(self):
        # self.click(self.product_loc)
        # self.click(self.product_1_loc)
        # self.click(self.product_2_loc)
        self.quit()

    def other(self):
        self.click(self.next_loc)
        self.click(self.next_2_loc)
        self.click(self.next_3_loc)
        self.click(self.next_4_loc)

class TestLogin(object):
    """
    登录用例
    """
    po = Login()

    def setup_class(self):
        TestLogin.po.login_base()

    data1 = [('账号不存在1', 'FS00000', 'Aa123456'), ('密码错误', 'FS001808', '123456')]
    @pytest.mark.parametrize('expect,username,password', data1)
    def test_login_fail(self, expect, username, password):
        """
        账号不存在、密码错误
        """
        TestLogin.po.login_action(username, password)
        try:
            actual = TestLogin.po.login_username_password_error(expect)
            assert expect in actual
            logger.info('断言成功，实际值【{}】 包含 期望值【{}】'.format(actual, expect))
        except:
            logger.error('断言失败，实际值【{}】 未包含 期望值【{}】'.format(actual, expect))
            expect = '失败截图'
            raise
        finally:
            TestLogin.po.screenshot_img(expect)

    data2 = [('下一步', 'FS001808', 'Aa123456')]
    @pytest.mark.parametrize('expect,username,password', data2)
    def test_login_success(self, expect, username, password):
        """
        登录成功
        """
        TestLogin.po.login_action(username, password)
        try:
            actual = TestLogin.po.login_success(expect)
            assert actual, expect
            logger.info('断言成功，实际值【{}】 等于 期望值【{}】'.format(actual, expect))
        except:
            logger.error('断言失败，实际值【{}】 不等于 期望值【{}】'.format(actual, expect))
            raise
        finally:
            TestLogin.po.screenshot_img('登录成功')

    def teardown_class(self):
        """
        登出，关闭app
        """
        # TestLogin.po.other()
        TestLogin.po.driver_quit()
        pass
