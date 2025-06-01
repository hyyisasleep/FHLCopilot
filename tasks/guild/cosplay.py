import numpy as np

from module.base.timer import Timer
from module.base.utils import get_color
from module.config.utils import is_under_maintenance
from module.exception import RequestHumanTakeover
from module.logger import logger
from module.ocr.ocr import Ocr, DigitCounter
from tasks.base.page import page_guild_cosplay

from tasks.base.ui import UI
from tasks.daily.assets.assets_daily_password import PSW_INPUT_BOX_CHECK
from tasks.guild.assets.assets_guild_cosplay import *


class CelebrityNameOcr(Ocr):
    pass


class Cosplay(UI):
    """
    名士演绎


    """

    STATUS_FLOWER = 6

    def run(self, skip_first_screenshot=True):
        logger.hr("Cosplay", level=1)
        if is_under_maintenance():
            logger.info("Social function is under maintenance, stop run cosplay script")
            return
        remain_times = 4
        if self.config.stored.SendStatusTimes.is_expired():
            self.config.stored.SendStatusTimes.clear()
        else:
            remain_times = self.config.stored.SendStatusTimes.get_remain()
        if remain_times == 0:
            logger.info("Today has sent 4 cosplay status, stop")
            return

        self.ui_ensure(page_guild_cosplay)

        flower = self.status_ocr()
        # 开发送动态界面
        cnt = 0
        while 1:
            if flower < self.STATUS_FLOWER:
                logger.info("Flower is not enough, stop")
                break
            # 发送动态每天领经验上限4次
            if cnt >= remain_times:
                break
            result = self.send_status()
            new_flower = self.status_ocr()
            if result == -1:
                logger.info("Flower is not enough, stop")
                self._close_status_popup()
                break
            # OCR和超时总有一个是准的吧
            if (flower - new_flower == self.STATUS_FLOWER) or result:
                cnt += 1
            flower = new_flower
            logger.info(f"Send status {cnt} times")
        # 写config
        self.config.stored.SendStatusTimes.add(cnt)

    def send_status(self, skip_first_screenshot=True):
        logger.hr("Send one status", level=2)
        if not self._open_send_status_popup():
            return 0
        if not self._switch_region():
            return 0
        return self._input_text_then_send_close()

    def _open_send_status_popup(self, skip_first_screenshot=True):
        timeout = Timer(5).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Can't open send status popup,stop")
                return False
            if self.appear(SEND_STATUS):
                logger.info("Send status popup is stable")
                return True
            if self.appear_then_click(OPEN_STATUS_POPUP):
                continue

    def _switch_region(self, skip_first_screenshot=True):
        timeout = Timer(5).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Can't switch region,stop")
                return False
            if self.appear(SWITCH_REGION_FINISH):
                logger.info("Switch region to gu-ren-wan-qian")
                return True
            if self.appear_then_click(SWITCH_REGION_TO_GRWQ):
                continue
            if self.appear_then_click(NEED_SWITCH_REGION):
                continue

    def _input_text_then_send_close(self, skip_first_screenshot=True) -> int:
        """
        Return:
            1: successful
            0: timeout
            -1: flower is not enough( when ocr fail
        """
        clicked = False
        timeout = Timer(10).start()
        prev = np.mean(get_color(self.device.image, STATUS_POPUP_BACKGROUND.area))
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get input text timeout,break")
                return 0
            if self.appear(FLOWER_NOT_ENOUGH_WARNING):
                logger.info("Flower is not enough, stop")
                return -1
            if clicked:
                cur = np.mean(get_color(self.device.image, STATUS_POPUP_BACKGROUND.area))
                if abs(cur - prev) > 30:
                    logger.info("Background color is changed, send successfully")
                    return 1
            if self.handle_level_up():
                continue
            if self.appear(INPUT_TEXT_FINISH):
                # 发送，理论上需要点两次，一次关
                self.appear_then_click(SEND_STATUS, interval=1)
                clicked = True
                continue
            if self.appear(PSW_INPUT_BOX_CHECK):
                self.device.input_text('咩咩咩咩')
                continue
            if self.appear_then_click(OPEN_INPUT_BOX):
                continue

    def handle_level_up(self,interval=5):
        if self.appear_then_click(LEVEL_UP_CHECK,interval):
            logger.info("Find Level up page")
            return True

    def _close_status_popup(self, skip_first_screenshot=True):
        timeout = Timer(10).start()
        prev = np.mean(get_color(self.device.image, STATUS_POPUP_BACKGROUND.area))
        clicked = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Can't close popup, need human takeover")
                raise RequestHumanTakeover
            if clicked:
                cur = np.mean(get_color(self.device.image, STATUS_POPUP_BACKGROUND.area))
                if cur - prev > 50:
                    logger.info("Background color is changed, send successfully")
                    return True
            if self.handle_level_up():
                continue
            if self.appear_then_click(CLOSE_STATUS_POPUP_CONFIRM):
                clicked = True
                continue

            if self.appear_then_click(CLOSE_STATUS_POPUP):
                continue

    def status_ocr(self):
        flower_num, _, total = DigitCounter(OCR_FLOWER).ocr_single_line(self.device.image)

        # name = CelebrityNameOcr(OCR_CELEBRITY_NAME).ocr_single_line(self.device.image)
        return flower_num  # , name


if __name__ == '__main__':
    ui = Cosplay('fhlc')
    ui.device.screenshot()
    ui.run()
