

from module.base.timer import Timer
from module.exception import GameNotRunningError
from module.logger import logger
from tasks.base.assets.assets_base_page import  BACK

from tasks.base.page import page_main

from tasks.login.assets.assets_login import *
from tasks.login.sign_in import SignInHandler


# from tasks.login.cloud import LoginAndroidCloud


class Login(SignInHandler):  # , LoginAndroidCloud):



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
                logger.info('Game is loading')
                self.device.stuck_record_clear()
                app_timer.reset()
                orientation_timer.reset()
                continue

            if self.appear(LOGIN_DOWNLOADING, interval=5):
                logger.info('Game resources downloading')
                self.device.stuck_record_clear()
                app_timer.reset()
                orientation_timer.reset()
                continue
            # 更新数据下载完成后有个弹窗提示重启
            if self.appear_then_click(UPDATE_FINISH_CONFIRM):
                logger.info("Game resources downloading finish")
                self.device.stuck_record_clear()
                app_timer.reset()
                orientation_timer.reset()
                continue

            # Login
            if self.is_in_login_confirm(interval=5):
                self.device.click(LOGIN_CONFIRM)
                login_success = True
                continue

            # Additional

            # 更新公告
            if self.appear_then_click(CLOSE_UPDATE_NOTICE):
                logger.info("Close update notification")
                continue
            # 有的时候有卡池和主线广告
            if self.appear_then_click(CLOSE_LOGIN_ADVERTISEMENT):
                logger.info("Skip main story or banner notification")
                continue
            # 金戈至尊赛结英广告
            if self.appear_then_click(CLOSE_JINGEZHIZUN_NOTICE):
                logger.info("Skip jin-ge-zhi-zun notice")
                continue
            # 翻截图看到的，大雪归鸿在登陆界面提示你拿未领取月卡奖励
            # 但是点完领取后会弹出reward弹窗，下面是能看到pagemain的检查标志的。。。
            # TODO:哪天不登陆测试一下？
            if self.appear_then_click(GET_LOST_MONTHLY_CARD_REWARD):
                logger.info("Get unclaimed monthly card reward")
                continue
            if self.handle_daily_sign_in_reward():
                continue
            # 处理签到+占卜
            if self.handle_guessing_celebrity_sign_in():
                continue
            if self.handle_activity_ticket_sign_in():
                continue

            # TODO:处理活动十连签到
            if self.handle_time_limit_sign_in():
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

if __name__ == "__main__":
    ui = Login('fhlc')
    ui.app_start()
