import os
from datetime import datetime
from operator import truediv, itemgetter

from sympy.codegen.ast import ContinueToken

from module.base.timer import Timer

from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.assets.assets_base_page import TAOYUAN_CHECK, TAOYUAN_GOTO_GAME
from tasks.base.assets.assets_base_popup import GET_REWARD

from tasks.base.page import page_taoyuan, page_taoyuan_meal, page_taoyuan_furniture, page_taoyuan_affair, \
    page_taoyuan_game
from tasks.base.ui import UI

from tasks.taoyuanju.assets.assets_taoyuanju import *


class Taoyuanju(UI):

    def run(self):
        """
        Run get support reward task
        """
        logger.hr('Taoyuanju affair', level=1)
        # self.ui_ensure(page_cattery)
        # 主页去桃源居，有祝福就领\
        # self.ui_ensure(page_taoyuan)
        self.ui_goto(page_taoyuan)
        # 领午晚饭体力
        self._get_lunch_and_dinner()
        # 处理事务
        self._deal_with_affairs()
        # TODO:领事务印象的10通宝
        self._get_affairs_impression_reward()

        # 拜访拿花
        self._visit_other()
        # 打造随机家具
        self._build_random_furniture()
        # 五天一回转化满的考工冶图道具
        self._convert_kaogong()

        self.ui_goto_main()

        self.config.task_delay(server_update=True)

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
                    break
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

        logger.info('Going to deal with taoyuan affair')
        timeout = Timer(5).start()
        skip_first_screenshot = True
        self.ui_goto(page_taoyuan_affair)

        #has_build = False
        start_deal = False
        affair_cnt = 0
        # ocr_affair =
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.info("Get taoyuan affair timeout")
                break
            # ocr_affair = Digit(DEAL_WITH_AFFAIR_START)
            # num = ocr_affair.ocr_single_line(self.device.image)
            # 显示事务0，不用做
            if self.appear(DEAL_WITH_AFFAIR_FINISH):
                if start_deal:
                    logger.info("Finish deal with affair")
                    break
                else:
                    logger.info("No need deal with affair")
                    break
            if not start_deal and self.appear_then_click(DEAL_WITH_AFFAIR_START):
                logger.info("Start deal with affair")
                start_deal = True
                continue
            # 1已经选过了就点2
            if self.appear_then_click(CHOOSE_AFFAIR_1):
                # start_deal = True
                affair_cnt += 1
                logger.info(f"Finish {affair_cnt} affair")
                timeout.reset()
                continue
            if self.appear_then_click(CHOOSE_AFFAIR_2):
                affair_cnt += 1
                logger.info(f"Finish {affair_cnt} affair with choice 2")
                timeout.reset()
                continue
            # 只写handle_reward每次点完事务都要点一次领奖？怪了
            if self.appear(GET_REWARD):
                self.handle_reward()
                continue


        self.ui_goto(page_taoyuan)




        pass

    def _visit_other(self):
        pass

    def _build_random_furniture(self):

        timeout = Timer(5).start()
        skip_first_screenshot = True
        self.ui_goto(page_taoyuan_furniture)
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

            if self.appear(BUILD_FURNITURE_FINISH):
                logger.info("No need build furniture")
                break

            if timeout.reached():
                logger.info("Get build furniture timeout")
                break

            #ocr看百工图数量
            bgt_ocr = Digit(BAIGONGTU_NUM,lang=self.config.LANG)
            num = bgt_ocr.ocr_single_line(self.device.image)


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

    def _goto_taoyuan_game_if_full(self)->bool:
        skip_first_screenshot = False
        timeout = Timer(1).start()
        full = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if not full and timeout.reached():
                logger.info("No need convert baigongtu")
                return False
            if full:
                if self.appear(GAME_CONVERT_CHECK):
                    return True
                if self.appear_then_click(GAME_GOTO_CONVERT):
                    logger.info("Go to convert ticket")
                    continue
            if self.appear(GAME_BAIGONGTU_FULL_CHECK):
                timeout.reset()
                full = True
                continue

        return False

    def _convert_kaogong(self):
        self.ui_goto(page_taoyuan_game)

        if self._goto_taoyuan_game_if_full():
            logger.info('Going to convert baigongtu')

            # 直接拉到10
            # self._item_amount_set(10, BAIGONGTU_AMOUNT_OCR, BAIGONGTU_AMOUNT_MINUS, BAIGONGTU_AMOUNT_PLUS)

            # 点确定转换
            timeout = Timer(1).start()
            has_convert = False
            skip_first_screenshot = False
            finish = False
            while 1:
                if skip_first_screenshot:
                    skip_first_screenshot = False
                else:
                    self.device.screenshot()
                if finish:
                    break
                if self.appear(BAIGONGTU_AMOUNT_LOCKED):
                    self.appear_then_click(BAIGONGTU_CONVERT_CLOSE)
                    finish = True
                    continue
                if timeout.reached():
                    logger.info("Get confirm to convert bgt timeout")
                    break

                if self.appear_then_click(BAIGONGTU_AMOUNT_PLUS,interval=0.3):
                    logger.info("add a item")
                    timeout.reset()
                    continue

                if self.appear_then_click(BAIGONGTU_CONVERT_CONFIRM):
                    continue
                if self.handle_reward():
                    logger.info("Convert baigontu finished")
                    timeout.reset()
                    has_convert = True
                    continue




            self.ui_goto(page_taoyuan)
    # 抄自 stamina
    def _item_amount_set(
            self,
            amount: int,
            ocr_button: ButtonWrapper,
            minus_button: ButtonWrapper,
            plus_button: ButtonWrapper,
            skip_first_screenshot=True,
    ):
        import cv2 as cv
        logger.info(f'Item amount set to {amount}')
        ocr = Digit(ocr_button, lang=self.config.LANG)
        interval = Timer(1, count=3)
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            current = ocr.ocr_single_line(cv.cvtColor(self.device.image,cv.COLOR_BGR2GRAY))
            if not current:
                continue
            # End
            if current == amount:
                logger.info(f'At target amount')
                break
            # Click
            if interval.reached():
                diff = amount - current
                if diff > 0:
                    _ = self.appear(plus_button)  # Search button
                    self.device.multi_click(plus_button, n=abs(diff))
                    interval.reset()
                elif diff < 0:
                    _ = self.appear(minus_button)  # Search button
                    self.device.multi_click(minus_button, n=abs(diff))
                    interval.reset()
                else:
                    logger.error(f'Invalid world diff: {diff}')


    def _get_affairs_impression_reward(self):
        """
        领10通宝，之后再写吧
        要是没研究明白列表拖拽可以领一次切到历程再切回来。。。这样红点又回到第一个位置了

        """
        pass



ui = Taoyuanju('src')
ui.device.screenshot()
ui.run()
#ui._convert_kaogong()
# 测桃源居这仨字在不同背景下能不能被检测到，目前用了三张全检测到了
# 王阳明那个洞天没图，等遇到bug再说吧
# path = r'D:\myProject\FHLCopilot\testPicFolder'
# for file in os.listdir(path):
#     ui.image_file = os.path.join(path,file)
#     print(f"{file}:{ui.appear(TAOYUAN_CHECK)}")

# ui.image_file = r"C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20240907-192155.png"
#
# print(ui.appear(GAME_BAIGONGTU_FULL_CHECK,similarity=0.6))




