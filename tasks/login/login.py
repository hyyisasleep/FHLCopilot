from module.base.timer import Timer
from module.exception import GameNotRunningError
from module.logger import logger
from tasks.base.assets.assets_base_page import CLOSE_LOGIN_ADVERTISEMENT, BACK, CLOSE_UPDATE_NOTICE
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.login.assets.assets_login import LOGIN_CONFIRM, LOGIN_LOADING, DAILY_SIGN_IN, \
    ACTIVITY_SIGN_IN_GIFT, ACTIVITY_SIGN_IN_GIFT_LOCKED, DIVINE_CHECK  # , USER_AGREEMENT_ACCEPT


# from tasks.login.cloud import LoginAndroidCloud


class Login(UI):  # , LoginAndroidCloud):

    def handle_activity_sign_in_gift(self):
        """
        活动期间的签到
        #TODO: 多天后的屏幕适配
        """
        if self.appear_then_click(ACTIVITY_SIGN_IN_GIFT):
            logger.info("Get activity sign in gift")
            return True
            # TODO: 判断补签还有除了第一天之外的位置会不会变QAQ
        # 检测已领取，不然直接点back不确定会卡到哪
        appear = self.appear(ACTIVITY_SIGN_IN_GIFT_LOCKED,interval=5)
        if appear and self.appear_then_click(BACK):
            logger.info("Close activity sign in gift page")
            return True
        return False

    def handle_sign_in_reward(self):
        """
         处理签到弹窗
        """
        if self.appear_then_click(DAILY_SIGN_IN):
            logger.info("Sign in")
            return True
        if self.handle_reward():
            logger.info("Get sign in reward")
            # if self.handle_reward():
            #     logger.info("Get 5-day sign in reward")
            # 占卜吧
            return True

        if self.appear(DIVINE_CHECK):
            self.appear_then_click(BACK, interval=2)
            logger.info("Sign in finish")

            return True
        return False
    def _handle_app_login(self):
        """
        Pages:
            in: Any page
            out: page_main

        Raises:
            GameStuckError:
            GameTooManyClickError:
            GameNotRunningError:
        """
        logger.hr('App login')
        orientation_timer = Timer(5)
        startup_timer = Timer(5).start()
        app_timer = Timer(5).start()
        login_success = False

        while 1:
            # Watch if game alive
            if app_timer.reached():
                if not self.device.app_is_running():
                    logger.error('Game died during launch')
                    raise GameNotRunningError('Game not running')
                app_timer.reset()
            # Watch device rotation
            if not login_success and orientation_timer.reached():
                # Screen may rotate after starting an app
                self.device.get_orientation()
                orientation_timer.reset()

            self.device.screenshot()

            # End
            # Game client requires at least 5s to start
            # The first few frames might be captured before app_stop(), ignore them
            if startup_timer.reached():
                if self.ui_page_appear(page_main):
                    logger.info('Login to main confirm')
                    break

            # Watch resource downloading and loading
            if self.appear(LOGIN_LOADING, interval=5):
                logger.info('Game resources downloading or loading')
                self.device.stuck_record_clear()
                app_timer.reset()
                orientation_timer.reset()

            # Login
            if self.is_in_login_confirm(interval=5):
                self.device.click(LOGIN_CONFIRM)
                login_success = True
                continue
            # if self.appear_then_click(USER_AGREEMENT_ACCEPT):
            #     continue
            # Additional
            # 更新公告，没测上😓
            # 好了不知道为什么现在每次启动都会出现这个
            if not login_success and self.appear_then_click(CLOSE_UPDATE_NOTICE):
                logger.info("Close update notification")
                continue
            # 有的时候有卡池和主线广告
            if self.appear_then_click(CLOSE_LOGIN_ADVERTISEMENT):
                logger.info("Skip main story or banner notification")
                continue

            if self.handle_activity_sign_in_gift():
                continue

            # 处理签到+占卜
            if self.handle_sign_in_reward():
                continue
            # 处理活动签到礼物

            # if self.handle_popup_confirm():
            #     continue
            # if self.ui_additional():
            #     continue

        return True

    def handle_app_login(self):
        logger.info('handle_app_login')
        self.device.screenshot_interval_set(1.0)
        self.device.stuck_timer = Timer(300, count=300).start()
        try:
            self._handle_app_login()
        finally:
            self.device.screenshot_interval_set()
            self.device.stuck_timer = Timer(60, count=60).start()

    def app_stop(self):
        logger.hr('App stop')
        # if self.config.is_cloud_game:
        #     self.cloud_exit()
        self.device.app_stop()

    def app_start(self):
        logger.hr('App start')
        self.device.app_start()

        # if self.config.is_cloud_game:
        #     self.device.dump_hierarchy()
        #     self.cloud_enter_game()
        # else:
        self.handle_app_login()

    def app_restart(self):
        logger.hr('App restart')
        self.device.app_stop()
        self.device.app_start()
        self.handle_app_login()
        # if self.config.is_cloud_game:
        #     self.device.dump_hierarchy()
        #     self.cloud_enter_game()
        # else:
        #

        self.config.task_delay(server_update=True)


ui = Login('src')
ui.app_start()
# ui.handle_activity_sign_in_gift()
# ui.app_restart()
# az = Login('src')
# az.image_file = r'C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20240905-194258.png'
#
# print(az.appear(CLOSE_LOGIN_ADVERTISEMENT))