from module.base.timer import Timer
from module.config.utils import get_server_datetime
from module.logger import logger
from module.ocr.ocr import Ocr,Digit
from tasks.PVP.assets.assets_pvp_jin_ge_yan_wu import *

from tasks.base.assets.assets_base_page import JINGEYANWU_CHECK,JINGEYANWU_GOTO_NO_REWARD_PREPARE
from tasks.base.page import page_jingeyanwu, page_jinge_prepare
from tasks.base.ui import UI

import time
from datetime import datetime, timedelta

class JinGeLevelOCR(Ocr):

    Char2Num = {'乾':10,'九':9,'八':8,'七':7,'六':6,'五':5,'四':4,'三':3,'二':2,'一':1}
    def after_process(self, result):
        result = super().after_process(result)
        for key in self.Char2Num:
            if key in result:
                value = self.Char2Num[key]
                return value
        return 0


def wait_for_start():
    """
    七段以上等金戈启动的
    """

    logger.info("Wait JinGe Start")
    # 金戈开启时间段
    morning_window = (11, 14)  # 11:00 - 14:00
    evening_window = (19, 21)  # 19:00 - 21:00

    # 获取当前时间
    now = get_server_datetime()
    current_hour = now.hour

    # 检查当前时间是否在指定的时间段内
    if (morning_window[0] <= current_hour < morning_window[1]) or (
            evening_window[0] <= current_hour < evening_window[1]):
        return True

    # 计算离下一个时间段最近的时间
    if current_hour < morning_window[0]:
        next_time = datetime(now.year, now.month, now.day, morning_window[0], 0)
    elif morning_window[1] <= current_hour < evening_window[0]:
        next_time = datetime(now.year, now.month, now.day, evening_window[0], 0)
    elif current_hour >= evening_window[1]:
        next_time = datetime(now.year, now.month, now.day + 1, morning_window[0], 0)  # 明天的11点
    else:
        return True
    # 计算剩余时间并每分钟输出一次
    while True:
        remaining_time = next_time - datetime.now()
        remaining_hours, remaining_minutes = divmod(remaining_time.seconds // 60, 60)

        logger.info(f"Remaining waiting time: {remaining_hours:02}:{remaining_minutes:02}")
        # 到了
        if remaining_time <= timedelta(minutes=1):
            return True

        time.sleep(60)


class JinGeYanWu(UI):

    # todo:
    # 七段以上按时间启动 每天只打三把，按时间上号打
    # 骁武魂的绿字识别效率有点惨

    def run(self):
        # self.wait_until_11()
        logger.hr('Clear jin ge talisman', level=1)
        # from datetime import datetime

        while 1:
            self.device.screenshot()
            self.ui_ensure(page_jingeyanwu)
            # 七段以上限时打金戈


            talisman_num, soul_num = self.pvp_ocr()

            # 获取金戈段位
            level = int(self.jin_ge_level_ocr())
            logger.info(f"Now level is {level}")
            # 写到config方便查看
            self.config.stored.JinGeLevel.value = level
            self.config.stored.TalismanToClean.value = talisman_num
            if level > 7:
                # 七段以上限时打金戈，
                wait_for_start()
            if level == 9:
                self.handle_buy_super_cat_ball_when_arrive_level_nine()



            if self.appear(JINGEYANWU_GOTO_NO_REWARD_PREPARE):
                logger.info("JinGe is not open this time, stop")
                break
            if talisman_num == 0 and self.config.ClearJinGeTalisman_EndWhenTalismanIsClear:
                logger.info("No need Ge, stop")
                break
            #
            # current_time = datetime.now().hour
            # # current_hour = current_time.hour
            # if current_time > 21:
            #     break
            logger.hr("Start one pvp game", level=2)

            self.ui_ensure(page_jinge_prepare)
            self._run_pvp(soul_num == 500)

        self.ui_goto_main()

    def handle_buy_super_cat_ball_when_arrive_level_nine(self):
        if self.config.ClearJinGeTalisman_BuySuperCatBallWhenArriveRankNineEveryWeek:
            # 每周一清空
            if self.config.stored.BuySuperCatBall.is_expired():
                logger.info('JinGe BuySuperCatBall When arrive rank nine expired')
                self.config.stored.BuySuperCatBall.clear()
            if self.config.stored.BuySuperCatBall.value == 0:
                from tasks.base.page import page_shop
                from tasks.shop.assets.assets_shop_goods import PVP_JINGE_GOODS_SUPER_CAT_BALL
                from tasks.shop.ui import ShopUI

                logger.info("Level is in 9, stop to buy shop's item")
                self.ui_ensure(page_shop)
                shop_ui = ShopUI('fhlc')
                num = shop_ui.buy_goods(PVP_JINGE_GOODS_SUPER_CAT_BALL)
                if num > 0:
                    self.config.stored.BuySuperCatBall.add()
                self.ui_ensure(page_jingeyanwu)
            else:
                logger.info("Check cat Ball has been sold, continue")



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
        # move to jinge prepare page
        # if self.appear_then_click(START_MATCH_START, interval):
        #     # start_pvp = True
        #     return True
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



    def wait_until_11(self):
        # 获取当前时间
        import time
        from datetime import datetime, timedelta
        now = datetime.now()

        # 计算距离 11 点还有多少时间
        target_time = now.replace(hour=11, minute=2, second=0, microsecond=0)

        # 如果当前时间已经超过了 11 点，则设置为明天的 11 点
        if now > target_time:
            target_time += timedelta(days=1)

        # 计算剩余时间
        remaining_time = (target_time - now).total_seconds()

        # 等待直到 11 点
        print(f"等待 {remaining_time} 秒，直到 11 点...")
        time.sleep(remaining_time)

        print("到了 11 点，结束函数。")



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


