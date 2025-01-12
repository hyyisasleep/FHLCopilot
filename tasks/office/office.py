from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit

from tasks.base.page import page_office, page_office_furniture, page_office_jigsaw
from tasks.base.ui import UI

from tasks.office.affair import Affair

from tasks.office.jigsaw import Jigsaw
from tasks.office.meal import Meal

from tasks.office.assets.assets_office_furniture import *
from tasks.office.visit import Visit


class Office(UI):

    def run(self):
        """
        Run get support reward task
        """
        logger.hr('TaoYuan Office', level=1)

        self.device.screenshot()
        self.ui_ensure(page_office)
        # 处理事务
        finish_affair = Affair(self.config, self.device).run()
        # 打造随机家具 太简单了不放单独类写了。。。
        finish_furniture = self._build_random_furniture()
        # 拜访拿花
        if self.config.DailyQuestOptions_VisitOthersForClivia:
            Visit(self.config, self.device).run()
        # 转化考工图道具
        if self.config.DailyQuestOptions_TransKaoGongTicket:
            Jigsaw(self.config, self.device).run()

        with self.config.multi_set():
            if finish_affair:
                self.config.stored.OfficeAffair.set(finish_affair)
            if finish_furniture:
                self.config.stored.OfficeBuildFurniture.set(finish_furniture)


        self.ui_goto_main()


    def _build_random_furniture(self)->int:
        """
        Return:
            int: If finish
        """
        finish = 0
        timeout = Timer(10).start()
        skip_first_screenshot = True
        self.ui_ensure(page_office_furniture)
        logger.hr('Build random furniture', level=1)
        has_build = False
        bgt_num = 0
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()


            if self.appear(BUILD_FURNITURE_FINISH):
                if has_build:
                    logger.info("successfully build furniture")
                else:
                    logger.info("No need build furniture")
                finish = 1
                break

            if timeout.reached():
                logger.warning("Get build furniture timeout")
                break

            if bgt_num == 0:
                # 有点风险但是目前还没见过OCR失败的
                bgt_num = Digit(OCR_BAIGONGTU_NUM, lang=self.config.LANG).ocr_single_line(self.device.image)

            if not has_build and bgt_num < 30:
                logger.info("Bai-gong-tu is not enough, cancel building furniture")
                break
            if self.appear_then_click(BUILD_FURNITURE_CHECK):
                continue
            if self.appear_then_click(BUILD_FURNITURE_CONFIRM):
                has_build = True
                finish = 1
                continue

        self.ui_ensure(page_office)
        return finish

if __name__ == "__main__":
    ui = Office('fhlc')

