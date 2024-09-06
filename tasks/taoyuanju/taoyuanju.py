from datetime import datetime

import numpy as np

from module.base.timer import Timer
from module.base.utils import area_size, random_rectangle_vector_opted
from module.logger import logger
from module.ocr.ocr import Digit
# from module.ui.draggable_list import DraggableList
from tasks.base.assets.assets_base_page import (
    TAOYUAN_CHECK, MAIN_GOTO_TAOYUAN, BACK,
)
from tasks.base.page import page_taoyuan, page_taoyuan_meal
from tasks.base.ui import UI

from tasks.taoyuanju.assets.assets_taoyuanju import (
    LUNCH_FINISH,
    LUNCH_UNLOCK, BUILD_FURNITURE_CHECK, BUILD_FURNITURE_CONFIRM, BAIGONGTU_NUM)


class Taoyuanju(UI):

    def run(self):
        """
        Run get support reward task
        """
        logger.hr('Taoyuanju affair', level=1)
        # self.ui_ensure(page_cattery)
        # 主页去桃源居，有祝福就领
        self.ui_goto(page_taoyuan)

        # 领午晚饭体力
        # self._get_lunch_and_dinner()
        # 处理事务
        self._deal_with_affairs()
        # 拜访拿花
        self._visit_other()
        # 打造随机家具
        self._build_random_furniture()
        # 五天一回转化满的考工冶图道具
        self._convert_kaogong()

        self.ui_goto_main()

        self.config.task_delay(server_update=True)

    # def _goto_taoyuanju(self):
    #     skip_first_screenshot = False
    #     logger.info('Going to taoyuanju')
    #     while 1:
    #         if skip_first_screenshot:
    #             skip_first_screenshot = False
    #         else:
    #             self.device.screenshot()
    #
    #         if self.appear(TAOYUAN_CHECK):
    #             logger.info('Successfully in taoyuanju')
    #             break
    #         if self.appear_then_click(MAIN_GOTO_TAOYUAN):
    #             continue

    # 从其他子页面返回桃源居主页
    # def _return_taoyuanju(self):
    #     skip_first_screenshot = True
    #     logger.info('Return to taoyuanju')
    #     while 1:
    #         if skip_first_screenshot:
    #             skip_first_screenshot = False
    #         else:
    #             self.device.screenshot()
    #         if self.appear(TAOYUAN_CHECK):
    #             logger.info('Successfully in taoyuanju')
    #             break
    #         if self.appear_then_click(BACK):
    #             continue

    # def _goto_lunch_page(self):
    #
    #     skip_first_screenshot = True
    #     logger.info('Going to eat meal')
    #     while 1:
    #         if skip_first_screenshot:
    #             skip_first_screenshot = False
    #         else:
    #             self.device.screenshot()
    #
    #         if self.appear(TAOYUAN_LUNCH_PAGE_CHECK):
    #             logger.info('Successfully in meal page')
    #             return True
    #
    #         if self.appear_then_click(TAOYUAN_GOTO_LUNCH):
    #             continue

    def handle_get_power_back(self, state='lunch'):
        pass

    def _get_lunch_and_dinner(self):

        self.ui_goto(page_taoyuan_meal)
        skip_first_screenshot = True
        get_lunch = False
        get_dinner = False
        check = False
        timeout = Timer(5).start()

        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            current_time = datetime.now()
            current_hour = current_time.hour

            if 11 <= current_hour < 15:
                if self.appear(LUNCH_FINISH):
                    if get_lunch:
                        logger.info('Get lunch power')
                    else:
                        logger.info("No need get lunch")
                    check = True
                    continue
                if self.appear_then_click(LUNCH_UNLOCK, interval=5):
                    get_lunch = True
                    timeout.reset()
                    continue
            elif 17 <= current_hour < 22:
                # TODO: 用偏移量？省的同一张图截两遍
                self.handle_get_power_back('lunch')
                break
                pass
            elif 22 <= current_hour < 24:
                self.handle_get_power_back('lunch')
                self.handle_get_power_back('dinner')
                break
            else:
                logger.info(f"Now time is {current_hour} h,no need get power")
                break

            if timeout.reached():
                logger.info('Get meal timeout')
                break

        self.ui_goto(page_taoyuan)

    def _deal_with_affairs(self):
        pass

    def _visit_other(self):
        pass

    def _build_random_furniture(self):

        skip_first_screenshot = True
        logger.info('Going to build random furniture')
        has_build = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if has_build:
                logger.info("Success build furniture")
                break
            # TODO: ocr看百工图数量 回来写吧哈哈
            ocr = Digit(BAIGONGTU_NUM)
            result = ocr.ocr()
            num = ocr.format_result()
            if not has_build and num < 30:
                logger.info("baigongtu is not enough, cancel build furniture")
                break
            if self.appear_then_click(BUILD_FURNITURE_CHECK):
                continue
            # TODO:以后要是还有确定框就抽象成函数
            if self.appear_then_click(BUILD_FURNITURE_CONFIRM):
                has_build = True
                continue

        self.ui_goto(page_taoyuan)

    def _convert_kaogong(self):
        pass


ui = Taoyuanju('src')
ui.device.screenshot()
ui.run()

#
# ui.image_file = r'C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\午晚饭素材\MuMu12-20240906-113039.png'
# #
# print(ui.appear(LUNCH_FINISH))
