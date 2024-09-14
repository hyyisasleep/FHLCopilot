from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.JinGe.assets.assets_JinGe import *
from tasks.base.page import page_jingeguan, page_jingeyanwu
from tasks.base.ui import UI


class ShaPanLunYi(UI):

    def run(self):

        logger.hr('Clear sha pan flag', level=1)

        while 1:
            # self.device.screenshot()

            # logger.info("?")
            # self.device.screenshot()
            # self.ui_ensure(page_shapanlunyi)

            logger.hr("Start one sha pan combat", level=2)
            self._run_shapan()
            flag_ocr = Digit(SHAPAN_FLAG_OCR, lang=self.config.LANG)
            flag_num = flag_ocr.ocr_single_line(self.device.image)
            if flag_num == 0:
                logger.info("No need clear flag")
                break

        # self.ui_goto_main()

    def _run_shapan(self, interval=5, skip_first_screenshot=False):
        finish = False
        has_start = False
        need_fresh = False
        while 1:

            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            timeout = Timer(20).start()

            if timeout.reached():
                logger.info("Get sha pan timeout")
                break
            if finish:
                break
            if self.appear_then_click(SHAPAN_REFRESH_CONFIRM):
                logger.info("Refresh")
                finish = True
                continue

            if self.appear_then_click(SHAPAN_GET_REWARD_CONFIRM):
                # logger.info("Get win reward")
                need_fresh = True
                continue
            if need_fresh and self.appear_then_click(SHAPAN_REFRESH):
                logger.info("Click refresh")
                continue
            if has_start and self.appear_then_click(SHAPAN_REFRESH):
                # self.handle_popup()
                logger.info("Click get reward")
                continue
            if not has_start and self.appear(SHAPAN_REWARD_LOCK,interval,similarity=0.9,):
                logger.info("Have got last round's reward,need refresh")
                need_fresh = True
                continue
            if self.appear(SHAPAN_COMBAT_CHECK, interval):
                logger.info("JIAN JUN continue")
                self.device.stuck_record_clear()
                timeout.reset()
                has_start = True
                continue
            if not has_start and self.appear_then_click(SHAPAN_COMBAT_PREPARE, interval):
                logger.info("E BA JIAN JUN prepare")
                continue
            if self.appear_then_click(SHAPAN_COMBAT_START, interval):
                logger.info("Start JIAN JUN combat")
                continue

            if self.handle_reward(interval):
                logger.info("Get pvp reward")

                continue





if __name__ == '__main__':
    ui = ShaPanLunYi('src')
    ui.device.screenshot()
    # print(ui.is_in_main())
    ui.run()
    # ui.image_file = r"C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20240908-190406.png"
    # print(ui.pvp_ocr())
