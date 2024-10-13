from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.PVP.assets.assets_pvp_JinGeYanWu import *
from tasks.base.page import page_jingeyanwu
from tasks.base.ui import UI


class JinGeYanWu(UI):

    # todo:
    # 七段以上按时间启动 每天只打三把，按时间上号打
    # 骁武魂的绿字识别效率有点惨

    def run(self):
        """
        Run get support reward task
        """
        logger.hr('Clear jin ge talisman', level=1)
        # from datetime import datetime

        while 1:
            self.device.screenshot()
            self.ui_ensure(page_jingeyanwu)
            talisman_num, soul_num = self.pvp_ocr()
            if talisman_num == 0:
                logger.info("No need pvp")
                break
            #
            # current_time = datetime.now().hour
            # # current_hour = current_time.hour
            # if current_time > 21:
            #     break
            logger.hr("Start one pvp game", level=2)
            self._run_pvp(soul_num == 500)

        self.ui_goto_main()

    def handle_use_xiaowu_soul(self, use_soul=False, interval=5):
        if use_soul:
            if self.appear_then_click(USE_SOUL_CONFIRM, interval):
                logger.info("Xiaowu soul is full, use it")
                return True
        else:
            if self.appear_then_click(USE_SOUL_CANCEL, interval):
                logger.info("Don't use xiaowu soul")
                return True
        return False

    def handle_pvp_combat(self, interval=5) -> bool:
        if self.appear_then_click(FINISH_CONFIRM, interval):
            return True
        if self.appear(WIN_CHECK, interval):
            logger.info("Get win")
            return True
        if self.appear(FAIL_CHECK, interval):
            logger.info("Get fail")
            return True
        if self.appear(FORMATION_CHECK, interval):
            logger.info("Combat is in formation")
            self.device.stuck_record_clear()
            # timeout.reset()
            return True
        if self.appear_then_click(MANUAL_COMBAT, similarity=0.95):
            logger.info("Turn to auto pvp")
            return True
        if self.appear(COMBAT_CHECK, interval):
            logger.info("Combat continue")
            self.device.stuck_record_clear()
            # timeout.reset()
            return True
        if self.appear(START_COMBAT_CHECK, interval):
            logger.info("Combat start")
            # timeout.reset()
            return True
        if self.appear(MATCHING_CHECK, interval):
            logger.info("Matching continue")
            self.device.stuck_record_clear()

            return True

        if self.appear_then_click(START_MATCH_CONFIRM, interval):
            # start_pvp = True
            return True
        if self.appear_then_click(START_MATCH_FIGHT, interval):
            # start_pvp = True
            return True
        if self.appear_then_click(START_MATCH_START, interval):
            # start_pvp = True
            return True
        return False

    def pvp_ocr(self) -> [int, int]:
        talisman_ocr = Digit(TALISMAN_OCR, lang=self.config.LANG)
        num = talisman_ocr.ocr_single_line(self.device.image)
        soul_ocr = Digit(SOUL_OCR, lang=self.config.LANG)
        num2 = soul_ocr.ocr_single_line(self.device.image)
        return num, num2

    def _run_pvp(self, use_soul=False, interval=5, skip_first_screenshot=True):
        finish_pvp = False
        while 1:

            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            timeout = Timer(20).start()

            if timeout.reached():
                logger.info("Get pvp timeout")
                break
            if finish_pvp:
                logger.info("One combat finish")
                break

            if self.handle_reward(interval):
                logger.info("Get pvp reward")
                finish_pvp = True
                continue
                # 每周有段位结算

            if self.handle_pvp_combat(interval):
                timeout.reset()
                continue
            if self.handle_use_xiaowu_soul(use_soul, interval):
                timeout.reset()
                continue


if __name__ == '__main__':
    ui = JinGeYanWu('fhlc')
    ui.device.screenshot()

    ui.run()

