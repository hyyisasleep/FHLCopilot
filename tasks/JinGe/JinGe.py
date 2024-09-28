

from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.JinGe.assets.assets_JinGe import *
from tasks.base.page import page_jingeguan, page_jingeyanwu
from tasks.base.ui import UI



class JinGe(UI):

    # todo:
    # 每天只打三把，按时间上号打
    # 六段以下匹配

    def run(self):
        """
        Run get support reward task
        """
        logger.hr('Clear jin ge talisman', level=1)
        # self.ui_ensure(page_cattery)

        # self.ui_ensure(page_jingeyanwu)
        #
        from datetime import datetime

        while 1:
            # self.device.screenshot()
            #
            # logger.info("?")
            self.device.screenshot()
            self.ui_ensure(page_jingeyanwu)
            talisman_num, soul_num = self.pvp_ocr()
            if talisman_num == 0:
                logger.info("No need pvp")
                break
            current_time = datetime.now().hour
            # current_hour = current_time.hour
            if current_time > 21:
                break
            logger.hr("Start one pvp game", level=2)
            self._run_pvp(soul_num == 500)

        self.ui_goto_main()

    def handle_use_xiaowu_soul(self,use_soul=False,interval=5):
        if use_soul:
            if self.appear_then_click(PVP_USE_SOUL_CONFIRM, interval):
                logger.info("Xiaowu soul is full, use it")
                return True
        else:
            if self.appear_then_click(PVP_USE_SOUL_CANCEL, interval):
                logger.info("Don't use xiaowu soul")
                return True
        return False

    def handle_pvp_combat(self,interval=5) -> bool:
        if self.appear_then_click(PVP_FINISH_CONFIRM, interval):
            return True
        if self.appear(PVP_WIN_CHECK, interval):
            logger.info("Get win")
            return True
        if self.appear(PVP_FAIL_CHECK, interval):
            logger.info("Get fail")
            return True
        if self.appear(PVP_FORMATION_CHECK, interval):
            logger.info("Combat is in formation")
            self.device.stuck_record_clear()
            # timeout.reset()
            return True
        if self.appear_then_click(PVP_MANUAL_COMBAT,similarity=0.95):
            logger.info("Turn to auto pvp")
            return True
        if self.appear(PVP_COMBAT_CHECK, interval):
            logger.info("Combat continue")
            self.device.stuck_record_clear()
            #timeout.reset()
            return True
        if self.appear(PVP_START_COMBAT_CHECK, interval):
            logger.info("Combat start")
            #timeout.reset()
            return True
        if self.appear(PVP_MATCHING_CHECK, interval):
            logger.info("Matching continue")
            self.device.stuck_record_clear()

            return True

        if self.appear_then_click(PVP_START_MATCH_CONFIRM, interval):
            # start_pvp = True
            return True
        if self.appear_then_click(PVP_START_MATCH_FIGHT, interval):
            # start_pvp = True
            return True
        if self.appear_then_click(PVP_START_MATCH_START, interval):
            # start_pvp = True
            return True
        return False

    def pvp_ocr(self)->[int,int]:
        talisman_ocr = Digit(PVP_TALISMAN_OCR, lang=self.config.LANG)
        num = talisman_ocr.ocr_single_line(self.device.image)
        soul_ocr = Digit(PVP_SOUL_OCR, lang=self.config.LANG)
        num2 = soul_ocr.ocr_single_line(self.device.image)
        return num, num2

    def _run_pvp(self,use_soul=False,interval=5,skip_first_screenshot=True):
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
            if self.appear_then_click(PVP_SKIP_LAST_WEEK_LEVEL):
                continue
            if self.handle_pvp_combat(interval):
                timeout.reset()
                continue
            if self.handle_use_xiaowu_soul(use_soul,interval):
                timeout.reset()
                continue










if __name__ == '__main__':
    ui = JinGe('src')
    ui.device.screenshot()
    #print(ui.is_in_main())
    ui.run()
    # ui.image_file = r"C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20240908-190406.png"
    # print(ui.pvp_ocr())
