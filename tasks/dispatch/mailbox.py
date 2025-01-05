from module.base.timer import Timer
from module.logger import logger

from tasks.base.ui import UI
from tasks.dispatch.assets.assets_dispatch_mailbox import *


#领邮箱奖励
class Mailbox(UI):

    def run(self):
        """
        """
        logger.hr('Mailbox', level=1)
        self._mailbox()

    def _mailbox(self,skip_first_screenshot=True):
        timeout = Timer(10).start()

        # 在首页看邮箱要不要开，已经开了的话跳转到下个循环处理
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get mailbox timeout")
                return

            if self.appear(MAILBOX_CHECK):
                logger.info("Mailbox is open")
                break
            if self.appear(OPEN_MAILBOX_NO_REWARD):
                logger.info("No need open mailbox,return")
                return
            if self.appear_then_click(OPEN_MAILBOX):
                continue

        timeout.reset()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get mailbox reward timeout")
                break
            if self.appear(PRESENT_MAIL_LOCKED):
                logger.info("No mail with present")
                break
            if self.handle_reward():
                continue
            if self.appear_then_click(GET_UPDATE_MAIL_REWARD):
                continue
            if self.appear_then_click(UPDATE_MAIL_UNLOCK):
                logger.info("Has update reward mail")
                continue
            if self.appear_then_click(PRESENT_MAIL_UNLOCK):
                logger.info("Has mail to get present")
                # self.appear_then_click(ONE_SWEEP_GET_MAIL)
                continue



        if self.appear(MAILBOX_CHECK):
            self.close_popup(CLOSE_MAILBOX,BACKGROUND_CHECK)


if __name__ == "__main__":
    ui = Mailbox('fhlc')
    ui.device.screenshot()
    ui.run()