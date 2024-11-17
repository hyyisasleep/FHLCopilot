from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Ocr,Digit
from tasks.PVP.assets.assets_pvp_jin_ge_yan_wu import *
from tasks.base.assets.assets_base_page import JINGEYANWU_CHECK
from tasks.base.page import page_jingeyanwu
from tasks.base.ui import UI

class JinGeLevelOCR(Ocr):

    Char2Num = {'乾':10,'九':9,'八':8,'七':7,'六':6,'五':5,'四':4,'三':3,'二':2,'一':1}
    def after_process(self, result):
        result = super().after_process(result)
        for key in self.Char2Num:
            if key in result:
                value = self.Char2Num[key]
                return value
        return 0

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


            level = self.jin_ge_level_ocr()

            logger.info(f"Now level is {level}")
            # if level == 9:
            #     logger.info("Level is in 9, stop to buy shop's item")
            #     # TODO:写配置。。。
            #     break

            # if talisman_num == 0:
            #     logger.info("No need pvp")
            #     break
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

    def handle_rank_ten_mode_prepare(self,interval=2)->bool:
        # 上纵横之后的ban人环节
        if self.appear_then_click(BAN_CONFIRM, interval):
            logger.info("Give up banning character")
            return True
        if self.appear_then_click(BAN_CHECK,interval):
            return True
        if self.appear_then_click(CHOOSE_CHARACTER_UNLOCK,interval):
            logger.info("Choose character")
            return True
        if self.appear(CHOOSE_CHARACTER_LOCKED,interval):
            return True
        return False

    def handle_result_win_or_fail(self,interval=5)->bool:
        if self.appear(WIN_CHECK, interval):
            logger.info("Get win")
            return True
        if self.appear(FAIL_CHECK, interval):
            logger.info("Get fail")
            return True
        return False

    def handle_pvp_combat(self, interval=5) -> bool:
        if self.appear_then_click(FINISH_CONFIRM, interval):
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

    def jin_ge_level_ocr(self)->str:
        retry = 0
        while retry < 3:
            level_ocr = JinGeLevelOCR(OCR_JINGE_LEVEL,lang=self.config.LANG)
            res = level_ocr.ocr_single_line(self.device.screenshot())
            if res != 0:
                return res
            else:
                logger.info("Level OCR fail, try it again")
                retry+=1
        return res

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
            # 每局结束条件改为看到一局win或者fail之后再回到金戈演武界面，发现符为0之后没有获得奖励界面了
            #
            if finish_pvp and self.appear(JINGEYANWU_CHECK):
                logger.info("One combat finish")
                break

            if self.handle_reward(interval):
                logger.info("Get pvp reward")
                finish_pvp = True
                continue
            # 两个finish没事吧。。。
            if self.handle_result_win_or_fail(interval):
                finish_pvp = True
                continue

            if self.handle_rank_ten_mode_prepare(interval):
                timeout.reset()
                continue
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


