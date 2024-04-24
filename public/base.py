#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @@Author: zhangmoumou
# @@Create Date: 2022/8/22 10:49
# @@Modify Date: 2022/8/22 10:49
# @@Description: 保鱼通v1.0.4
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
import warnings
import logging
warnings.filterwarnings('ignore')
from branch import globalparam, read_yaml
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from branch.ocr_img import ocr_toast, ocr_picture_text
from public.methods import *
logger_air = logging.getLogger("airtest")
logger_air.setLevel(logging.ERROR)

logger = Log()

PICTUREPATH = globalparam.picture_path
PICLOCATEPATH = globalparam.pic_locate_path
ERRORFILE = globalparam.error_file
OCRPATH = globalparam.ocr_path

input_text = text

class PocoPackage(object):
    """
    基本方法的引用
    """
    def __init__(self):
        self.poco = PocoPackage.start_apps()
        self.env = globalparam.environment
        self.yaml = read_yaml.ReadYaml('baoyutong')

    @staticmethod
    def start_apps():
        """
        启动app
        """
        try:
            poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
            # 唤醒屏幕
            wake()
            # 左滑唤醒相机
            if poco("com.android.systemui:id/right_button").exists() is True:
                poco("com.android.systemui:id/right_button").swipe([-0.5731, 0.0193])
                poco("com.android.systemui:id/home").click()
            start_app('com.fs.diyi')
            ym = "com.netease.nie.yosemite/.ime.ImeService"
            shell("ime enable " + ym)
            shell("ime set " + ym)
            filepath = PICTUREPATH + '/' + '{}.jpg'.format('初始化截图')
            snapshot(filename=filepath, msg='初始化截图', quality=90, max_size=800)
            return poco
        except Exception as e:
            with open(ERRORFILE + '/error.txt', 'w') as f:
                f.write(str(e))
            logger.error('应用初始化失败：{}'.format(e))
            raise

    def _login(self, username, password):
        """
        登录操作
        """
        self.poco("com.fs.diyi:id/siv_bg_account_name").click()
        text(username)
        self.poco("com.fs.diyi:id/siv_bg_account_pwd").click()
        text(password)

    def switch_env(self):
        """
        切换环境
        :return:
        """
        try:
            env_dict = {
                'TEST': 'test',
                'PRE': 'pre',
                'RELEASE': 'prod'
            }
            if self.element_text("com.fs.diyi:id/tv_btn_right") == '同意':
                self.element_click("com.fs.diyi:id/tv_btn_right")
            if self.poco("com.fs.diyi:id/tv_title").exists() is True:
                self.poco("com.fs.diyi:id/tv_title").long_click()
                self.element_click("com.fs.diyi:id/tv_btn_{}".format(env_dict[self.env]))
            logger.info('切换到{}环境成功'.format(self.env))
        except:
            logger.error('切换到{}环境失败'.format(self.env))


    def login_common(self):
        """
        登录
        """
        try:
            username, password = map(str, self.yaml.get_url_user('moblie_code').split(','))
            # self.element_exist('com.fs.diyi:id/cl_title')
            # self.poco("com.fs.diyi:id/cl_title").wait_for_appearance(timeout=10)
            if self.poco("com.fs.diyi:id/cl_title").exists() is True:
                logger.info('已登录')
            else:
                # 手机号登录
                if (self.poco("com.fs.diyi:id/tv_title").exists() is True) and (self.poco("com.fs.diyi:id/tv_title").attr("text") == '使用须知'):
                    # 关闭使用须知弹窗
                    self.poco("com.fs.diyi:id/tv_btn_right").click()
                # 切换环境
                self.switch_env()
                self._login(username, password)
                self.poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring(
                    "android.widget.LinearLayout"). \
                    offspring("android.widget.ImageView").poco("com.fs.diyi:id/tv_btn_login").click()
                # 如果未进入首页，说明未勾选协议和隐私，勾选上后登录
                if self.poco("com.fs.diyi:id/cl_tab_home").exists() is False:
                    self.poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring(
                        "android.widget.LinearLayout").offspring("android.widget.ImageView").click()
                    self.poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring(
                            "android.widget.LinearLayout"). \
                        offspring("android.widget.ImageView").poco("com.fs.diyi:id/tv_btn_login").click()
                if self.poco("com.fs.diyi:id/cl_tab_home").exists() is True:
                    logger.info('登录成功')
                # 如果有新人指引，则关闭
                if self.poco("com.fs.diyi:id/tv_confirm0").exists() is True:
                    self.poco("com.fs.diyi:id/tv_confirm").click()
                    self.poco("com.fs.diyi:id/tv_confirm2").click()
                    self.poco("com.fs.diyi:id/tv_confirm3").click()
        except:
            logger.error('登录失败')
            raise

    def login_out(self):
        """
        退出登录，点击"我的"界面
        :return:
        """
        try:
            self.element_click("com.fs.diyi:id/cl_tab_mine")
            self.element_swipe("com.fs.diyi:id/scroll_container", swipe=[0.009, -0.3238])
            self.element_click(text="设置")
            self.element_click("com.fs.diyi:id/login_out")
            self.element_click("com.fs.diyi:id/tv_btn_right")
            return '登出成功'
        except:
            logger.error('退出登录失败')
            return '登出失败'

    def new_start_app(self):
        """
        启动app
        """
        try:
            start_app('com.fs.diyi')
            logger.info('打开APP成功')
        except:
            logger.error('打开APP失败')
            raise

    def new_start_app_wechat(self):
        """
        启动微信app
        """
        try:
            start_app('com.tencent.mm')
            logger.info('打开APP成功')
        except:
            logger.error('打开APP失败')
            raise

    def new_stop_app(self):
        """
        关闭app
        """
        try:
            stop_app('com.fs.diyi')
            logger.info('关闭APP成功')
        except:
            logger.error('关闭APP失败')
            raise

    def allure_screenshots(self, name):
        """
        截图并引入报告
        """
        try:
            filepath = PICTUREPATH + '/' + '{}.jpg'.format(name)
            snapshot(filename=filepath, msg=name, quality=90, max_size=800)
            with open(filepath, mode='rb') as f1:
                file = f1.read()
            allure.attach(file, '截图', allure.attachment_type.JPG)
        except:
            logger.error('报告【{}】截图失败'.format(name))
            raise

    def element_exist(self, locate, timeout=8):
        """
        判断元素是否存在，
        只针对poco()最基础的定位进行判断
        """
        try:
            end_time = time.time() + timeout
            while True:
                if self.poco(locate).exists() is True:
                    return True
                if time.time() > end_time:
                    return False
        except:
            logger.error('判断定位【{}】是否存在失败'.format(locate))
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            return False
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def element_exist_text(self, text, timeout=8):
        """
        判断元素是否存在，
        只针对poco()的text定位进行判断
        """
        try:
            end_time = time.time() + timeout
            while True:
                if self.poco(text="{}".format(text)).exists() is True:
                    return True
                if time.time() > end_time:
                    return False
        except:
            logger.error('判断定位【{}】是否存在失败'.format(text))
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            raise

    def element_swipe(self, locate=None, text=None, swipe=None, timeout=8):
        """
        判断元素是否存在，如果存在则滑动
        """
        try:
            end_time = time.time() + timeout
            while True:
                if locate is not None:
                    if self.poco(locate).exists() is True:
                        locats = self.poco(locate)
                        locats.swipe(swipe)
                        logger.info('元素【{}】等待并滑动成功'.format(locate))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并滑动失败'.format(locate))
                        raise TimeoutError
                else:
                    if self.poco(text="{}".format(text)).exists() is True:
                        locats = self.poco(text="{}".format(text))
                        locats.swipe(swipe)
                        logger.info('元素【text={}】等待并滑动成功'.format(text))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并滑动失败'.format(text))
                        raise TimeoutError
        except Exception as e:
            raise e
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def new_text(self, input, clear=0, enter=False, search=False):
        """
        输入文本
        """
        if clear > 0:
            for i in range(clear):
                keyevent("KEYCODE_DEL")
        return text(input, enter=enter, search=search)

    def element_click(self, locate=None, text=None, timeout=8):
        """
        判断元素存在后，进行点击操作
        """
        try:
            end_time = time.time() + timeout
            while True:
                if locate is not None:
                    if self.poco(locate).exists() is True:
                        self.poco(locate).click()
                        logger.info('元素【{}】等待并点击成功'.format(locate))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并点击失败'.format(locate))
                        raise '元素【{}】等待并点击失败'.format(locate)
                else:
                    if self.poco(text="{}".format(text)).exists() is True:
                        self.poco(text="{}".format(text)).click()
                        logger.info('元素【text={}】等待并点击成功'.format(text))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并点击失败'.format(text))
                        raise TimeoutError
        except Exception as e:
            logger.error('元素【{}】/【{}】等待并点击失败'.format(locate, text))
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def element_long_click(self, locate=None, text=None, duration=3, timeout=8):
        """
        判断元素存在后，进行点击操作
        """
        try:
            end_time = time.time() + timeout
            while True:
                if locate is not None:
                    if self.poco(locate).exists() is True:
                        # self.poco(locate).long_click()
                        self.poco(locate).swipe((0, 0), duration=duration)
                        logger.info('元素【{}】等待并长按成功'.format(locate))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并长按失败'.format(locate))
                        raise '元素【{}】等待并长按失败'.format(locate)
                else:
                    if self.poco(text="{}".format(text)).exists() is True:
                        # self.poco(text="{}".format(text)).long_click()
                        self.poco(text="{}".format(text)).swipe((0, 0), duration=duration)
                        logger.info('元素【text={}】等待并长按成功'.format(text))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并长按失败'.format(text))
                        raise TimeoutError
        except Exception as e:
            logger.error('元素【{}】/【{}】等待并长按失败'.format(locate, text))
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def element_input(self, locate=None, text=None, input='', clear=0, enter=False, search=False, timeout=8):
        """
        判断元素存在后，进行清空输入文本
        """
        try:
            end_time = time.time() + timeout
            while True:
                if locate is not None:
                    if self.poco(locate).exists() is True:
                        self.poco(locate).click()
                        # 全选删除
                        if clear == 1000:
                            self.element_long_click(locate)
                            if self.element_text(text="全选") == '全选':
                                self.element_click(text="全选")
                            else:
                                self.element_click("Select all")
                            keyevent("KEYCODE_DEL")
                        elif clear > 0:
                            for i in range(clear):
                                keyevent("KEYCODE_DEL")
                        input_text(input, enter=enter, search=search)
                        logger.info('元素【{}】等待并输入【{}】成功'.format(locate, input))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并输入【{}】失败'.format(locate, input))
                        raise '元素【{}】等待并点击失败'.format(locate)
                else:
                    if self.poco(text="{}".format(text)).exists() is True:
                        self.poco(text="{}".format(text)).click()
                        # 全选删除
                        if clear == 1000:
                            self.element_long_click(text="{}".format(text))
                            if self.element_text(text="全选") == '全选':
                                self.element_click(text="全选")
                            else:
                                self.element_click("Select all")
                            keyevent("KEYCODE_DEL")
                        elif clear > 0:
                            for i in range(clear):
                                keyevent("KEYCODE_DEL")
                        input_text(input, enter=enter, search=search)
                        logger.info('元素【text={}】等待并输入【{}】成功'.format(text, input))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并输入【{}】失败'.format(text, input))
                        raise TimeoutError
        except Exception as e:
            logger.error('元素【{}】/【{}】等待并输入【{}】失败'.format(locate, text, input))
            raise
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def picture_input(self, path, record_pos=(0.299, -0.955), resolution=(1080, 2340), vector=None, input='', clear=0,
                            enter=False, search=False, timeout=8, threshold=None):
        """
        根据图片定位等待，图片存在则清空输入文本
        """
        path_base = globalparam.pic_locate_path
        try:
            wait(Template(path_base + path, threshold, record_pos=record_pos,
                           resolution=resolution), timeout=timeout)
            touch(Template(path_base + path, record_pos=record_pos,
                           resolution=resolution))
            if clear == 1000:
                self.picture_swipe(path, record_pos=(0, 0), resolution=(1080, 2340), vector=[0, 0])
                self.element_click(text="全选")
                keyevent("KEYCODE_DEL")
            elif clear > 0:
                for i in range(clear):
                    keyevent("KEYCODE_DEL")
            input_text(input, enter=enter, search=search)
            logger.info('图片【{}】等待并输入【{}】成功'.format(path, input))
        except:
            logger.error('图片【{}】等待并输入【{}】失败'.format(path, input))
            raise
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def element_text(self, locate=None, text=None, timeout=8):
        """
        判断元素存在后，获取实际值
        """
        try:
            end_time = time.time() + timeout
            while True:
                if locate is not None:
                    if self.poco(locate).exists() is True:
                        actual_text = self.poco(locate).attr("text")
                        actual_name = self.poco(locate).get_name()
                        # 判断是否存在文本属性
                        if actual_text is not None:
                            actual = actual_text
                        # name属性为文本的才走此分支
                        elif (actual_name is not None) and 'com.fs' not in actual_name and 'android' not in actual_name:
                            actual = actual_name
                        else:
                            logger.warning('此元素【{}】无文本属性值，请使用截图定位方式获取'.format(locate))
                            return '未获取到文本值：None'
                        logger.info('元素【{}】等待并获取文本成功，结果为：{}'.format(locate, actual))
                        return actual
                    if time.time() > end_time:
                        logger.error('判断定位【{}】是否存在失败'.format(locate))
                        raise TimeoutError
                else:
                    if self.poco(text="{}".format(text)).exists() is True:
                        actual_text = self.poco(text="{}".format(text)).attr("text")
                        actual_name = self.poco(text="{}".format(text)).get_name()
                        # 判断是否存在文本属性
                        if actual_text is not None:
                            actual = actual_text
                        elif (actual_name is not None) and 'com.fs' not in actual_name and 'android' not in actual_name:
                            actual = actual_name
                        else:
                            logger.warning('此元素【text={}】无文本属性值，请使用截图定位方式获取'.format(text))
                            return '未获取到文本值：None'
                        logger.info('元素【text={}】等待并获取文本成功，结果为：{}'.format(text, actual))
                        return actual
                    if time.time() > end_time:
                        logger.error('判断定位【text={}】是否存在失败'.format(text))
                        raise TimeoutError
        except:
            logger.error('元素【{}&{}】未获取到文本值'.format(locate, text))
            return False

    def picture_click(self, path, record_pos=(0.299, -0.955), resolution=(1080, 2340), timeout=8, threshold=None):
        """
        根据图片定位等待，图片存在则点击
        """
        path_base = globalparam.pic_locate_path
        try:
            wait(Template(path_base + path, threshold, record_pos=record_pos,
                           resolution=resolution), timeout=timeout)
            touch(Template(path_base + path, record_pos=record_pos,
                           resolution=resolution))
            logger.info('图片【{}】等待并点击成功'.format(path))
        except:
            logger.error('图片【{}】等待并点击失败'.format(path))
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def picture_text(self, path, record_pos=(0.299, -0.955), resolution=(1080, 2340), timeout=8, threshold=None):
        """
        根据图片定位等待，图片存在则进行ocr识别获取文本
        """
        path_base = globalparam.pic_locate_path
        try:
            wait(Template(path_base + path, threshold, record_pos=record_pos,
                          resolution=resolution), timeout=timeout)
            acturl = ocr_picture_text(path_base + path)
            logger.info('图片【{}】等待并获取文本成功，结果为：{}'.format(path, acturl))
            return acturl
        except:
            logger.error('图片【{}】等待并获取文本失败'.format(path))
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            return False

    def picture_swipe(self, path, record_pos=(0.299, -0.955), resolution=(1080, 2340), vector=None,
                      timeout=8, threshold=None, duration=0.5):
        """
        根据图片定位等待，图片存在则滑动
        """
        path_base = globalparam.pic_locate_path
        try:
            wait(Template(path_base + path, threshold, record_pos=record_pos,
                           resolution=resolution), timeout=timeout)
            swipe(Template(path_base + path, record_pos=vector,
                       resolution=resolution), vector=vector, duration=duration)
            logger.info('图片【{}】等待并滑动成功'.format(path))
        except:
            logger.error('图片【{}】等待并滑动失败'.format(path))
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def new_clear_app(self):
        """
        清除应用数据
        :return:
        """
        try:
            clear_app('com.fs.diyi')
            start_app('com.fs.diyi')
            sleep(1)
            self.element_click("com.fs.diyi:id/timer_count")
            self.start_apps()
            if self.element_text("com.fs.diyi:id/tv_title") == '使用须知':
                # 关闭使用须知弹窗
                self.element_click("com.fs.diyi:id/tv_btn_right")
            self.switch_env()
            start_app('com.fs.diyi')
            logger.info('清除APP缓存数据成功')
        except:
            logger.error('清除APP缓存数据失败')
            raise

    def snapshot_img(self, name, file=PICTUREPATH):
        """
        截图
        :return:
        """
        try:
            filepath = file + '\\' + '{}.jpg'.format(name)
            snapshot(filename=filepath, msg=name, quality=90, max_size=800)
        except:
            logger.error('截图【{}】失败'.format(name))
            raise

    def ocr_text(self, name, locate=(70, 360, 310, 420)):
        """
        ocr识别文字
        :return:
        """
        try:
            self.snapshot_img(name, OCRPATH)
            text = ocr_toast(name, locate)
            print(text)
            return text
        except:
            logger.error(f'ocr识别【{name}】失败')
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def ocr_text_continue(self, expect_text, name, locate=(70, 360, 310, 420)):
        """
        ocr识别文字，循环识别，当识别到指定文本或者识别次数到达5次后则终止
        :param text：期望文本
        :param name：被识别图片
        :return:
        """
        try:
            n = 0
            while True:
                n += 1
                self.snapshot_img(name, OCRPATH)
                text = ocr_toast(name, locate)
                if (expect_text in text) or (text in expect_text):
                    return text
                if n > 5:
                    return '超出最大识别限制'
        except:
            logger.error(f'ocr持续识别【{name}】失败')
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def swipe_locate(self, pic_name='tpl1664095130876', start=(-0.416, -0.925)):
        """
        拖动操作，默认针对dokit
        """
        try:
            swipe(Template(PICLOCATEPATH + '/' + r"{}.png".format(pic_name), record_pos=start, resolution=(1080, 2400)),
                  vector=[-0.0634, 0.8163])
            logger.info('拖动控件成功')
        except:
            logger.error('拖动【{}.png】失败'.format(pic_name))
            raise
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def return_previous_page(self, num=1):
        """
        操作系统按键返回上一页
        :param num 返回次数
        """
        for i in range(num):
            self.element_click("com.android.systemui:id/back")

    def wechat_friends_share(self):
        # 点击微信按钮，分享到微信好友
        try:
            self.element_click("com.fs.diyi:id/tv_wxfriend_share")
            self.element_click("android.widget.ImageView")
            text("文件传输助手")
            self.element_click("com.tencent.mm:id/kpm")
            self.element_click("com.tencent.mm:id/guw")
            self.element_click("com.tencent.mm:id/gui")
        except:
            Log().info("元素不存在")
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            raise

    def wechat_moments_share(self):
        # 点击朋友圈按钮，分享到朋友圈
        try:
            self.element_click("com.fs.diyi:id/tv_wxcircle_share")
            self.element_click("com.tencent.mm:id/en")
        except:
            Log().info("元素不存在")
            raise

    def enterprise_wechat_friends_share(self):
        # 点击企业微信按钮，分享到企业微信好友
        try:
            self.element_click("com.fs.diyi:id/tv_enterprisewx_share")
            self.element_click("com.tencent.wework:id/l36")
            text("文件传输助手")
            self.element_click("com.tencent.wework:id/gbw")
            self.element_click("com.tencent.wework:id/ciq")
            self.element_click("com.tencent.wework:id/cin")
        except:
            Log().info("元素不存在")
            raise

    def copy_link_share(self):
        # 点击复制链接按钮，复制链接
        try:
            self.element_click("com.fs.diyi:id/tv_linkurl_share")
        except:
            Log().info("元素不存在")
            raise

    def element_click_any(self, *args, timeout=8):
        """
        点击多次, args可传，'xxxx'、'text=xxxx'
        """
        try:
            for locates in args:
                if 'text=' in locates:
                    split_text = locates.split('=')[-1]
                    print(split_text)
                    self.element_click(text=split_text, timeout=timeout)
                else:
                    self.element_click(locate=locates, timeout=timeout)
        except Exception as e:
            Log().error(f'元素定位多次点击失败：{e}')
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def picture_click_any(self, path, *args, timeout=8, threshold=None):
        """
        点击多次, args可传，'xxxx'、'text=xxxx'
        """
        base_path = f'\\{path}\\'
        try:
            for locates in args:
                self.picture_click(base_path + locates, timeout=timeout, threshold=threshold)
        except Exception as e:
            Log().error(f'图片定位多次点击失败：{e}')
        finally:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def element_text_any(self, *args, timeout=8):
        """
        点击获取元素文本, args可传，'xxxx'、'text=xxxx'
        """
        try:
            text_list = []
            for locates in args:
                if 'text=' in locates:
                    split_text = locates.split('=')[-1]
                    text = self.element_text(text=split_text, timeout=timeout)
                else:
                    text = self.element_text(locate=locates, timeout=timeout)
                text_list.append(text)
            if len(text_list) == 1:
                return text_list[0]
            else:
                return text_list
        except Exception as e:
            Log().error(f'元素定位多次点击失败：{e}')
            return False

    def picture_text_any(self, path, *args, timeout=8, threshold=None):
        """
        点击多次, args可传，'xxxx'、'text=xxxx'
        """
        try:
            text_list = []
            base_path = f'\\{path}\\'
            for locates in args:
                text = self.picture_text(base_path + locates, timeout=timeout, threshold=threshold)
                text_list.append(text)
            if len(text_list) == 1:
                return text_list[0]
            else:
                return text_list
        except Exception as e:
            Log().error(f'图片定位多次点击失败：{e}')
            return False

    def element_check_success(self, locates, expect=None, remarks=None, timeout=8):
        """
        进行操作（点击、滑动、输入），并校验操作后的结果是否正确
        """
        try:
            # 确定元素定位方式
            if 'text=' in locates:
                split_text = locates.split('=')[-1]
                text = self.element_text(text=split_text, timeout=timeout)
            else:
                text = self.element_text(locate=locates, timeout=timeout)
            # 确定备注，无备注则用获取的属性文本
            if remarks is None:
                remark = text
            else:
                remark = remarks
            # 判断属性文本是否存在
            if (expect is not None) and (text == expect):
                return f'{remark}存在'
            elif (expect is None) and (text is not False):
                return f'{remark}存在'
            else:
                return f'{remark}不存在'
        except Exception as e:
            return f'{remark}不存在，{e}'

    def element_check_success_any(self, locates_list: list, expect_list=None, remarks_list=None, timeout=8):
        result = []
        try:
            for num in range(len(locates_list)):
                if expect_list is None:
                    expect_list = [None, None, None]
                if remarks_list is None:
                    remarks_list = [None, None, None]
                locate, expect, remarks = locates_list[num], expect_list[num], remarks_list[num]
                # 确定元素定位方式
                if 'text=' in locate:
                    split_text = locate.split('=')[-1]
                    text = self.element_text(text=split_text, timeout=timeout)
                else:
                    text = self.element_text(locate=locate, timeout=timeout)
                # 确定备注，无备注则用获取的属性文本
                if remarks is None:
                    remark = text
                else:
                    remark = remarks
                # 判断属性文本是否存在
                if (expect is not None) and (text == expect):
                    result.append(f'{remark}存在')
                elif (expect is None) and (text is not False):
                    result.append(f'{remark}存在')
                else:
                    result.append(f'{remark}不存在')
            return result
        except Exception as e:
            Log().error(f'多元素校验失败：{e}')

    def effective_after_update_no_sure(self, locate=None, text=None, timeout=8):
        """
              判断元素存在后，获取实际值
              """
        try:
            end_time = time.time() + timeout
            while True:
                if locate is not None:
                    self.element_click_any(locate)
                    if self.poco(locate).exists() is True:
                        return self.element_text(locate)
                    else:
                        return '元素未找到'
                if text is not None:
                    self.element_click_any(text)
                    if self.poco(text="{}".format(text)).exists() is True:
                        return self.element_text(text)
                    else:
                        return '元素未找到'
        except Exception as e:
            Log().error(f'多元素校验失败：{e}')


class PocoPackageFx(object):
    """
    基本方法的引用
    """
    def __init__(self):
        self.poco = PocoPackageFx.start_app()
        self.env = globalparam.environment
        self.yaml = read_yaml.ReadYaml('Fx')

    @staticmethod
    def start_app():
        """
        启动app
        """
        try:
            poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
            # 唤醒屏幕
            wake()
            # 左滑唤醒相机
            if poco("com.android.systemui:id/right_button").exists() is True:
                poco("com.android.systemui:id/right_button").swipe([-0.5731, 0.0193])
                poco("com.android.systemui:id/home").click()
            start_app('com.tencent.mm')
            ym = "com.netease.nie.yosemite/.ime.ImeService"
            shell("ime enable " + ym)
            shell("ime set " + ym)
            filepath = PICTUREPATH + '/' + '{}.jpg'.format('初始化截图')
            snapshot(filename=filepath, msg='初始化截图', quality=90, max_size=800)
            return poco
        except Exception as e:
            with open(ERRORFILE + '/error.txt', 'w') as f:
                f.write(str(e))
            logger.error('应用初始化失败：{}'.format(e))
            raise

    def pocoFun(self):
        try:
            poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
            print("这是poco："+ str(poco))
            return poco
        except Exception as e:
            logger.error('应用初始化失败：{}'.format(e))

    def enterFx(self):
        """
        进入凡星小程序
        """
        # self.poco("android.widget.FrameLayout").offspring("com.tencent.mm:id/fj1").child(
        #     "android.widget.FrameLayout").offspring("com."
        #                                             "tencent.mm:id/e_a")[1].offspring("com.tencent.mm:id/fj3").child(
        #     "android.widget.LinearLayout").child("com."
        #                                          "tencent.mm:id/kd_")[2].offspring("com.tencent.mm:id/f2a").click()
        PocoPackageFx().element_click(text="发现")
        PocoPackageFx().element_click(text="小程序")
        PocoPackageFx().element_click(text="我的小程序")
        PocoPackageFx().switch_env()


    def switch_env(self):
        """
        切换环境
        :return:
        """
        print("当前环境："+self.env)
        try:
            if self.env == 'PRE':
                print('预发环境')
                self.element_click("com.tencent.mm:id/kem")
                self.picture_click("\\hanxiao\\tpl1681892234981.png", record_pos=(0.299, -0.955), resolution=(1080, 2340))
                self.picture_click("\\hanxiao\\tpl1681892502412.png", record_pos=(0.102, 0.718), resolution=(1080, 2340))
                # self.poco("com.tencent.mm:id/kai").child("android.widget.FrameLayout").child(
                #     "android.widget.LinearLayout").offspring("android:id/content").offspring(
                #     "androidx.recyclerview.widget.RecyclerView").child("android.widget.RelativeLayout")[0].offspring(
                #     "com.tencent.mm:id/i2m").click()
            elif self.env == 'TEST':
                print('测试环境')
                self.element_click(text="凡星名片")
                self.picture_click("\\hanxiao\\tpl1681892234981.png", record_pos=(0.299, -0.955), resolution=(1080, 2340))
                self.picture_click("\\hanxiao\\tpl1681892502412.png", record_pos=(0.102, 0.718), resolution=(1080, 2340))

            elif self.env == 'RELEASE':
                self.picture_click("\\hanxiao\\tpl1675756421012.png", record_pos=(-0.191, -0.789), resolution=(1080, 2340))
                self.picture_click("\\hanxiao\\tpl1681892234981.png", record_pos=(0.299, -0.955), resolution=(1080, 2340))
                self.picture_click("\\hanxiao\\tpl1681892502412.png", record_pos=(0.102, 0.718), resolution=(1080, 2340))
                # self.poco("com.tencent.mm:id/kai").child("android.widget.FrameLayout").child(
                #     "android.widget.LinearLayout").offspring("android:id/content").offspring(
                #     "androidx.recyclerview.widget.RecyclerView").child("android.widget.RelativeLayout")[1].offspring(
                #     "com.tencent.mm:id/i2m").click()
            logger.info('切换到{}环境成功'.format(self.env))
        except:
            logger.error('切换到{}环境失败'.format(self.env))
            raise

    def close_advertising(self):

        return
    def login_out(self):
        """
        退出登录，点击"我的"界面
        :return:
        """
        try:
            # self.new_stop_app()
            # self.new_start_app()
            # self.poco("com.fs.diyi:id/cl_tab_mine").wait_for_appearance(10)
            # self.poco("com.fs.diyi:id/cl_tab_mine").click()
            # self.poco("com.fs.diyi:id/scroll_container").swipe([0.009, -0.3238])
            # self.poco(text="设置").click()
            # self.poco("com.fs.diyi:id/login_out").click()
            # self.poco("com.fs.diyi:id/tv_btn_right").click()
            self.element_click(text="我的")
            # 点击退出登录
            self.element_click("android.widget.TextView")
            # 点击确定
            self.element_click("com.tencent.mm:id/gv3")
            self.new_stop_app()
        except:
            logger.error('退出登录失败')
            raise

    def new_start_app(self):
        """
        启动app
        """
        try:
            start_app('com.tencent.mm')
            logger.info('打开微信应用成功')
        except:
            logger.error('打开微信应用失败')
            raise

    def new_stop_app(self):
        """
        关闭app
        """
        try:
            stop_app('com.tencent.mm')
            logger.info('关闭微信应用成功')
        except:
            logger.error('关闭微信应用失败')
            raise

    def allure_screenshots(self, name):
        """
        截图并引入报告
        """
        try:
            filepath = PICTUREPATH + '/' + '{}.jpg'.format(name)
            snapshot(filename=filepath, msg=name, quality=90, max_size=800)
            with open(filepath, mode='rb') as f1:
                file = f1.read()
            allure.attach(file, '截图', allure.attachment_type.JPG)
        except:
            logger.error('报告【{}】截图失败'.format(name))
            raise

    def element_exist(self, locate, timeout=8):
        """
        判断元素是否存在，
        只针对poco()最基础的定位进行判断
        """
        try:
            end_time = time.time() + timeout
            while True:
                if self.poco(locate).exists() is True:
                    return True
                if time.time() > end_time:
                    return False
        except:
            logger.error('判断定位【{}】是否存在失败'.format(locate))
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            raise

    def element_exist_text(self, text, timeout=8):
        """
        判断元素是否存在，
        只针对poco()的text定位进行判断
        """
        try:
            end_time = time.time() + timeout
            while True:
                if self.poco(text="{}".format(text)).exists() is True:
                    return True
                if time.time() > end_time:
                    return False
        except:
            logger.error('判断定位【{}】是否存在失败'.format(text))
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            raise

    def element_swipe(self, locate=None, text=None, swipe=None, timeout=8):
        """
        判断元素是否存在，如果存在则滑动
        """
        try:
            end_time = time.time() + timeout
            while True:
                if locate is not None:
                    if self.poco(locate).exists() is True:
                        locats = self.poco(locate)
                        locats.swipe(swipe)
                        logger.info('元素【{}】等待并滑动成功'.format(locate))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并滑动失败'.format(locate))
                        raise TimeoutError
                else:
                    if self.poco(text="{}".format(text)).exists() is True:
                        locats = self.poco(text="{}".format(text))
                        locats.swipe(swipe)
                        logger.info('元素【text={}】等待并滑动成功'.format(text))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并滑动失败'.format(text))
                        raise TimeoutError
        except Exception as e:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            raise e

    def element_click(self, locate=None, text=None, timeout=8):
        """
        判断元素存在后，进行点击操作
        """
        try:
            end_time = time.time() + timeout
            while True:
                if locate is not None:
                    if self.poco(locate).exists() is True:
                        self.poco(locate).click()
                        logger.info('元素【{}】等待并点击成功'.format(locate))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并点击失败'.format(locate))
                        raise TimeoutError
                else:
                    if self.poco(text="{}".format(text)).exists() is True:
                        self.poco(text="{}".format(text)).click()
                        logger.info('元素【text={}】等待并点击成功'.format(text))
                        break
                    if time.time() > end_time:
                        logger.error('元素【{}】等待并点击失败'.format(text))
                        raise TimeoutError
        except Exception as e:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            raise e

    def element_text(self, locate=None, text=None, timeout=8):
        """
        判断元素存在后，获取实际值
        """
        try:
            end_time = time.time() + timeout
            while True:
                if locate is not None:
                    if self.poco(locate).exists() is True:
                        actual_text = self.poco(locate).attr("text")
                        actual_name = self.poco(locate).get_name()
                        # 判断是否存在文本属性
                        if actual_text is not None:
                            actual = actual_text
                        # name属性为文本的才走此分支
                        elif (actual_name is not None) and 'com.fs' not in actual_name and 'android' not in actual_name:
                            actual = actual_name
                        else:
                            logger.warning('此元素【{}】无文本属性值，请使用截图定位方式获取'.format(locate))
                            return '未获取到文本值：None'
                        logger.info('元素【{}】等待并获取文本成功，结果为：{}'.format(locate, actual))
                        return actual
                    if time.time() > end_time:
                        logger.error('判断定位【{}】是否存在失败'.format(locate))
                        raise TimeoutError
                else:
                    if self.poco(text="{}".format(text)).exists() is True:
                        actual_text = self.poco(text="{}".format(text)).attr("text")
                        actual_name = self.poco(text="{}".format(text)).get_name()
                        # 判断是否存在文本属性
                        if actual_text is not None:
                            actual = actual_text
                        elif (actual_name is not None) and 'com.fs' not in actual_name and 'android' not in actual_name:
                            actual = actual_name
                        else:
                            logger.warning('此元素【text={}】无文本属性值，请使用截图定位方式获取'.format(text))
                            return '未获取到文本值：None'
                        logger.info('元素【text={}】等待并获取文本成功，结果为：{}'.format(text, actual))
                        return actual
                    if time.time() > end_time:
                        logger.error('判断定位【text={}】是否存在失败'.format(text))
                        raise TimeoutError
        except:
            logger.error('元素【{}&{}】未获取到文本值'.format(locate, text))
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            return False

    def picture_click(self, path, record_pos=(0.299, -0.955), resolution=(1080, 2340), timeout=9, threshold=None):
        """
        根据图片定位等待，图片存在则点击
        """
        path_base = globalparam.pic_locate_path
        try:
            wait(Template(path_base + path, threshold, record_pos=record_pos,
                           resolution=resolution), timeout=timeout)
            touch(Template(path_base + path, record_pos=record_pos,
                           resolution=resolution))
            logger.info('图片【{}】等待并点击成功'.format(path))
        except:
            logger.error('图片【{}】等待并点击失败'.format(path))
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def picture_text(self, path, record_pos, resolution, timeout=8, threshold=None):
        """
        根据图片定位等待，图片存在则进行ocr识别获取文本
        """
        path_base = globalparam.pic_locate_path
        try:
            wait(Template(path_base + path, threshold, record_pos=record_pos,
                          resolution=resolution), timeout)
            acturl = ocr_picture_text(path_base + path)
            logger.info('图片【{}】等待并获取文本成功，结果为：{}'.format(path, acturl))
            return acturl
        except:
            logger.error('图片【{}】等待并获取文本失败'.format(path))
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            return False

    def new_clear_app(self):
        """
        清除应用数据
        :return:
        """
        try:
            clear_app('com.fs.diyi')
            start_app('com.fs.diyi')
            self.element_click("com.fs.diyi:id/timer_count")
            self.start_app()
            if self.element_text("com.fs.diyi:id/tv_title") == '使用须知':
                # 关闭使用须知弹窗
                self.element_click("com.fs.diyi:id/tv_btn_right")
            self.switch_env()
            start_app('com.fs.diyi')
            logger.info('清除APP缓存数据成功')
        except:
            logger.error('清除APP缓存数据失败')
            raise

    def snapshot_img(self, name, file=PICTUREPATH):
        """
        截图
        :return:
        """
        try:
            filepath = file + '\\' + '{}.jpg'.format(name)
            snapshot(filename=filepath, msg=name, quality=90, max_size=800)
        except:
            logger.error('截图【{}】失败'.format(name))
            raise

    def ocr_text(self, name, locate=(80, 420, 290, 450)):
        """
        ocr识别文字
        :return:
        """
        try:
            self.snapshot_img(name, OCRPATH)
            text = ocr_toast(name, locate)
            return text
        except:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def ocr_text_continue(self, expect_text, name, locate=(70, 360, 310, 420)):
        """
        ocr识别文字，循环识别，当识别到指定文本或者识别次数到达5次后则终止
        :param text：期望文本
        :param name：被识别图片
        :return:
        """
        try:
            n = 0
            while True:
                n += 1
                self.snapshot_img(name, OCRPATH)
                text = ocr_toast(name, locate)
                if (expect_text in text) or (text in expect_text):
                    return text
                if n > 5:
                    return '超出最大识别限制'
        except:
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)

    def swipe_locate(self, pic_name='tpl1664095130876', start=(-0.416, -0.925)):
        """
        拖动操作，默认针对dokit
        """
        try:
            swipe(Template(PICLOCATEPATH + '/' + r"{}.png".format(pic_name), record_pos=start, resolution=(1080, 2400)),
                  vector=[-0.0634, 0.8163])
            logger.info('拖动控件成功')
        except:
            logger.error('拖动【{}.png】失败'.format(pic_name))
            name = int(round(time.time() * 1000000))
            self.allure_screenshots(name)
            raise

if __name__ == "__main__":
    # PocoPackage().element_click_any("text=计划书", "com.fs.diyi:id/tv_btn_right", "com.android.systemui:id/back",
    #                                 "com.android.systemui:id/back", "text=产品对比")
    # PocoPackage().picture_click_any("zhangyancheng", "tpl1682562887784.png", "tpl1682563123203.png")
    # PocoPackage().element_check_success("text=聊天信息", expect='聊天信息', remarks='聊天信息入口存在')
    # PocoPackage().element_check_success_any(["text=聊天信息", "com.fs.diyi:id/tv_btn_edit", "text=保单"],
    #                                     ['聊天信息1', '编辑', '保单'], ['聊天信息入口', '编辑', '保单'])
    # PocoPackage().picture_input("\\zhangyancheng\\tpl1683527267274.png", input="111", clear=1000)
    PocoPackage().ocr_text_continue('下载完成', "下载图片成功", locate=(120, 380, 250, 405))

