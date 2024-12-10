from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_main, page_profile

from tasks.base.ui import UI
from tasks.daily.assets.assets_daily_password import *

#每日签到密令
class DailyPassword(UI):

    def run(self):
        """
        """
        logger.hr('Open wechat to sign in', level=1)
        # 跳转到互动界面
        from tasks.daily.getpsw import wechat_sign_in_and_get_password
        psw = wechat_sign_in_and_get_password()
        if psw == "" or psw is None:
            logger.warning("Can't get today's password,break")
            return
        else:
            logger.info(f"Get password:{psw}")

        logger.hr('Fill password', level=1)
        self.ui_ensure(page_profile)
        self.fill_password(psw)
        self.ui_ensure(page_main)
        self.config.task_delay(server_update=True)

    def fill_password(self,psw, interval=2, skip_first_screenshot=True):
        if self._open_psw_popup():
            self._fill_password(psw)
            self._close_psw_popup()




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

    def _fill_password(self,psw,skip_first_screenshot=True):
        timeout = Timer(10).start()
        # 填密令
        input_text = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get fill password timeout")
                return False

            if self.appear(FILL_PSW_FAILED):
                logger.info("Sign in failed, maybe because password is incorrect?")
                return True
            if self.appear(FILL_PSW_FAILED_BEFORE_FILLED):
                logger.info("Sign in failed, because password has been used" )
                return True
            if self.handle_reward():
                continue
            if self.appear_then_click(FILL_CONFIRM_UNLOCK):
                continue
            if input_text and self.appear_then_click(PSW_INPUT_BOX_CONFIRM):
                continue
            if self.appear(PSW_INPUT_BOX_CHECK):
                self.device.input_text(psw)
                input_text = True
                timeout.reset()
                continue
            if self.appear_then_click(OPEN_PSW_INPUT_BOX):
                continue

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
            if self.appear_then_click(CLOSE_PSW_POPUP):
                continue


if __name__ == "__main__":
    ui = DailyPassword("fhlc")
    ui.device.screenshot()
    ui.run()