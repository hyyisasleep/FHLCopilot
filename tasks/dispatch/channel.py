from module.base.timer import Timer
from module.logger import logger

from tasks.base.ui import UI
from tasks.dispatch.assets.assets_dispatch import GOTO_KYLIN_PAGE, GOTO_KYLIN_PAGE_NO_REWARD
from tasks.dispatch.assets.assets_dispatch_channel import *

#每天在世界频道发言两次
class Channel(UI):

    def run(self):
        """
        """
        logger.hr('Send message twice in word channel', level=1)
        # 跳转到互动界面
        self.send_message()

        # self.config.task_delay(server_update=True)

    def send_message(self, interval=2, skip_first_screenshot=True):

        timeout = Timer(10).start()
        count = 0
        # skip_first_screenshot = False

        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get open channel page timeout")
                return
            if self.appear(CHANNEL_CHECK):
                logger.info("Channel page is open, continue")
                break
            if self.appear_then_click(GOTO_CHANNEL):
                logger.info("Open channel page")
                continue
        timeout.reset()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get send message in world channel timeout")
                break
            if count >= 2:
                if self.appear(GOTO_KYLIN_PAGE) or self.appear(GOTO_KYLIN_PAGE_NO_REWARD):
                    break
                if self.appear_then_click(CLOSE_CHANNEL):
                    logger.info("Close channel page")
                    continue

            else:
                if self.appear(SEND_UNLOCK):
                    self.interval_reset(SEND_UNLOCK)
                    if self.appear_then_click(SEND_ICON_GANBEI):
                        logger.info("Send ganbei icon")
                        count += 1
                        timeout.reset()
                        continue

                    if self.appear_then_click(GOTO_ICON_GANBEI_PAGE):
                        logger.info("Switch to shijun's icon page")
                        continue

                    if self.appear_then_click(OPEN_ICON):
                        logger.info("Open icon menu")
                        continue







if __name__ == "__main__":
    ui = Channel("fhlc")
    ui.device.screenshot()
    ui.run()