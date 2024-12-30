from datetime import datetime

from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_office_meal, page_office
from tasks.base.ui import UI
from tasks.office.assets.assets_office_meal import *


class Meal(UI):

    def run(self, skip_first_screenshot=True):
        """

        """
        logger.hr('Get meal power', level=1)
        self.ui_ensure(page_office_meal, skip_first_screenshot)
        self._get_lunch_and_dinner()
        self.ui_ensure(page_office)

        self.config.task_delay(target=self._get_delay_target())


    @staticmethod
    def _get_delay_target():
        """
        懒得在SRC找怎么写延迟的了直接自己写了一个（对不起
        领完之后推迟到下一次午晚饭或第二天的午饭，但是目前没考虑失败
        """
        now = datetime.now()
        # current_hour = current_time.hour
        next_time = now
        hour = now.hour
        if 0 <= hour < 11:
            next_time = datetime(now.year, now.month, now.day, 11, 0)
        if 11 <= hour < 17:
            next_time = datetime(now.year, now.month, now.day,17, 0)
        elif 17 <= hour < 24:
            next_time = datetime(now.year, now.month, now.day + 1,11, 0)
        return next_time

    def _get_lunch_and_dinner(self):
        now = datetime.now()
        if now.hour < 11:
            logger.info("Time is not up yet, no need to have a meal")
            return
        self._get_meal_power("lunch",LUNCH_UNLOCK,LUNCH_FINISH,LUNCH_GETBACK)

        if now.hour >= 17:
            self._get_meal_power("dinner", DINNER_UNLOCK,DINNER_FINISH,DINNER_GETBACK)

    def _get_meal_power(self,state:str,unlock_button:ButtonWrapper,finish_button:ButtonWrapper,get_back_button:ButtonWrapper,skip_first_screenshot=True):
        """
        午晚饭一个套路只是用的button不一样

        Args:
            state:str,"lunch" or "dinner"
            unlock_button:ButtonWrapper,
            finish_button:ButtonWrapper
            get_back_button:ButtonWrapper
            skip_first_screenshot:bool

        """

        get_back = self.config.MealPower_UseTongBaoBuyExpiredPower
        timeout = Timer(10).start()
        finish = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.info(f'Get {state} meal timeout')
                break

            if not get_back:
                if self.appear(get_back_button):
                    logger.info(f"Have unclaimed {state} power, config choose ignore")
                    break
            if self.appear(finish_button):
                if finish:
                    logger.info(f'Get {state} power')
                else:
                    logger.info(f"No need get {state} power")
                # check = True
                break
            if self.appear_then_click(unlock_button):
                finish = True
                timeout.reset()
                continue
            if get_back:
                if self.appear_then_click(GET_BACK_CONFIRM):
                    logger.info(f"Use tong bao to get {state} power")
                    continue
                if self.appear_then_click(get_back_button):
                    continue






    #
    # def _get_lunch_and_dinner(self,current_hour:int):
    #
    #     skip_first_screenshot = True
    #     get_lunch = False
    #     get_dinner = False
    #     timeout = Timer(5).start()
    #
    #     while 1:
    #         if skip_first_screenshot:
    #             skip_first_screenshot = False
    #         else:
    #             self.device.screenshot()
    #
    #         if timeout.reached():
    #             logger.info('Get meal timeout')
    #             break
    #
    #         if 11 <= current_hour < 15:
    #             if self.appear(LUNCH_FINISH):
    #                 if get_lunch:
    #                     logger.info('Get lunch power')
    #                 else:
    #                     logger.info("No need get lunch")
    #                 # check = True
    #                 break
    #             if self.appear_then_click(LUNCH_UNLOCK, interval=5):
    #                 get_lunch = True
    #                 timeout.reset()
    #                 continue
    #         elif 17 <= current_hour < 22:
    #
    #             self.handle_get_power_back('lunch')
    #
    #             if self.appear(DINNER_FINISH):
    #                 if get_dinner:
    #                     logger.info('Get dinner power')
    #                 else:
    #                     logger.info("No need dinner lunch")
    #                 # check = True
    #                 break
    #             if self.appear_then_click(DINNER_UNLOCK, interval=5):
    #                 get_dinner = True
    #                 timeout.reset()
    #                 continue
    #             continue
    #         elif 22 <= current_hour < 24:
    #             self.handle_get_power_back('lunch')
    #             self.handle_get_power_back('dinner')
    #             continue
    #         else:
    #             logger.info(f"Now time is {current_hour} h,no need get power")
    #             break

    #
    # def handle_get_power_back(self, state='lunch'):
    #     #
    #
    #     if state == 'lunch' and self.appear(LUNCH_GETBACK):
    #         logger.info("Still have unclaimed lunch stamina")
    #         if self.appear_then_click(GET_BACK_CONFIRM):
    #             return True
    #         if self.appear_then_click(LUNCH_GETBACK):
    #             logger.info("Use tongbao to exchange lunch stamina")
    #         return True
    #     if state == 'dinner' and self.appear(DINNER_GETBACK):
    #         logger.info("Still have unclaimed dinner stamina")
    #         if need_get_back and self.device.click(DINNER_GETBACK):
    #             logger.info("Use tongbao to exchange lunch stamina")
    #         return True
    #     return False

if __name__ == "__main__":
    ui = Meal('fhlc')
    ui.device.screenshot()
    ui.run()