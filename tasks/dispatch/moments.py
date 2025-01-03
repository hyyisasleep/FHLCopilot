
from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import  DigitCounter
from tasks.base.page import page_moments
from tasks.base.ui import UI
from tasks.dispatch.assets.assets_dispatch_moments import *


class MomentsOCR(DigitCounter):
    pass


class Moments(UI):

    # 感觉还在抽风，明天跑一下试试
    def run(self):
        """
        """
        logger.hr('Give 3 heart in moments', level=1)
        # 跳转到知交圈界面
        self.ui_ensure(page_moments)
        self._give_heart()
        self.ui_goto_main()



        # self.config.task_delay(server_update=True)

    def _give_heart(self, skip_first_screenshot=True):

        self._wait_until_moments_page_stabled()
        timeout = Timer(10).start()

        #bug: sometimes will click 2 heart in different location??
        CLICK_HEART.match_template(self.device.image)
        # CLICK_HEART_OK.load_offset(CLICK_HEART)
        interval = Timer(0.5).start()
        cur_count = 0
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get moments timeout")
                break
            if self.appear(HEART_REWARD_DISAPPEAR):
                logger.info("Get moments reward finish")
                break
            if self.handle_reward():
                continue
            if cur_count >= 3:
                if self.appear_then_click(HEART_REWARD_UNLOCK):
                    logger.info("Click finish")
                continue
            if interval.reached():
                interval.reset()
                cur_count,_,total_count = MomentsOCR(OCR_COUNT,lang=self.config.LANG).ocr_single_line(self.device.image)
                if self.device.click(CLICK_HEART):
                    continue


    def _wait_until_moments_page_stabled(self, skip_first_screenshot=True):
        """
        Returns:
            bool: True if wait success, False if wait timeout.

        Pages:
            in: page_guide, Survival_Index
        """
        # Wait until moments page stabled
        timeout = Timer(5, count=3).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            # End
            if timeout.reached():
                logger.warning('Wait until moments stabled timeout')
                return False

            # End
            if self.appear(PAGE_STABLE_CHECK):
                logger.info("Moments page is stable")
                return True


if __name__ == "__main__":
    ui = Moments("fhlc")
    ui.device.screenshot()
    ui.run()