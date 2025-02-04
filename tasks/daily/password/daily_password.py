from module.base.timer import Timer
from module.config.utils import get_server_weekday, deep_get
from module.logger import logger
from tasks.base.page import page_main, page_profile

from tasks.base.ui import UI
from tasks.daily.assets.assets_daily_password import *

#每日签到密令
class DailyPassword(UI):

    def run(self)->bool:
        """
        Return:
            bool: If successfully sign in and fill psw
        """
        logger.hr('Open wechat to sign in', level=1)

        if self.config.stored.OneWeekPasswordList.is_expired():
            logger.info('Clear last week password')
            self.config.stored.OneWeekPasswordList.clear()


        # 老铁不这么干不能读字符串内容= =。。。。
        config_path = deep_get(self.config.data,'DailyPassword.DailyPassword.WechatInstallPath')
        logger.info(f'Config wechat path:{config_path}')


        from tasks.daily.password.wechat_sign_in import wechat_sign_in_and_get_password
        psw = wechat_sign_in_and_get_password(config_path)
        if psw == "" or psw is None:
            logger.warning("Can't get today's password,break")
            return False
        else:
            logger.info(f"Get password:{psw}")


        today = get_server_weekday()

        # 更新到config里
        # logger.info(self.config.stored.OneWeekPasswordList.p2)
        self.config.stored.OneWeekPasswordList.write_daily_password(today+1,psw)

        logger.hr('Fill password', level=1)
        self.ui_ensure(page_profile)
        finish = self.fill_password(psw)
        if finish:
            self.config.stored.AutoDailyPassword.set(1)
        self.ui_ensure(page_main)
        # self.config.task_delay(server_update=True)
        return finish

    def fill_password(self,psw)->bool:
        if self._open_psw_popup():
            finish = self._fill_password(psw)
            self._close_psw_popup()
            return finish
        return False


    def _open_psw_popup(self,skip_first_screenshot=True):
        timeout = Timer(10).start()

        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.appear(PSW_POPUP_CHECK):
                logger.info("Password popup is open")
                return True
            if timeout.reached():
                logger.warning("Get timeout when open password popup")
                return False
            if self.appear_then_click(OPEN_PSW_POPUP):
                # logger.info("Open password page")
                continue

        return False

    def _fill_password(self,psw,skip_first_screenshot=True)->bool:
        timeout = Timer(10).start()
        # 填密令,
        finish = False
        has_filled_text = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get fill password timeout")
                break
            # 用确定框由橙变灰判定是否填完密令
            if has_filled_text and self.appear(FILL_CONFIRM_LOCKED):
                logger.info("Sign in completed")
                finish = True
                break
            if self.appear(FILL_PSW_FAILED):
                logger.info("Sign in failed, maybe because password is incorrect?")
                break
            if self.appear(FILL_PSW_FAILED_BEFORE_FILLED):
                logger.info("Sign in failed, because password has been used" )
                finish = True
                break
            if self.handle_reward():
                continue
            if self.appear_then_click(FILL_CONFIRM_UNLOCK,similarity=0.95):
                has_filled_text = True
                timeout.reset()
                continue

            if self.appear(PSW_INPUT_BOX_CHECK,interval=3):
                self.device.input_text(psw)
                timeout.reset()
                continue
            if self.appear_then_click(PSW_INPUT_BOX_CONFIRM):
                continue
            if self.appear_then_click(OPEN_PSW_INPUT_BOX):
                continue
        return finish

    def _close_psw_popup(self,skip_first_screenshot=True):
        timeout = Timer(10).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get fill password timeout")
                return
            if self.appear(PSW_POPUP_CLOSED_CHECK):
                logger.info("Password page is closed")
                break
            if self.appear_then_click(CLOSE_PSW_POPUP,interval=3):
                continue


if __name__ == "__main__":
    ui = DailyPassword("fhlc")
    ui.device.screenshot()
    ui.run()