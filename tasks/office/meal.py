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

        self.config.task_delay(server_update=True)

    def _get_lunch_and_dinner(self):

        skip_first_screenshot = True
        get_lunch = False
        get_dinner = False
        timeout = Timer(5).start()

        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.info('Get meal timeout')
                break

            current_time = datetime.now()
            current_hour = current_time.hour

            if 11 <= current_hour < 15:
                if self.appear(LUNCH_FINISH):
                    if get_lunch:
                        logger.info('Get lunch power')
                    else:
                        logger.info("No need get lunch")
                    # check = True
                    break
                if self.appear_then_click(LUNCH_UNLOCK, interval=5):
                    get_lunch = True
                    timeout.reset()
                    continue
            elif 17 <= current_hour < 22:
                # 没研究明白偏移量，截了两张图:)
                self.handle_get_power_back('lunch')

                if self.appear(DINNER_FINISH):
                    if get_dinner:
                        logger.info('Get dinner power')
                    else:
                        logger.info("No need dinner lunch")
                    # check = True
                    break
                if self.appear_then_click(DINNER_UNLOCK, interval=5):
                    get_dinner = True
                    timeout.reset()
                    continue
                continue
            elif 22 <= current_hour < 24:
                self.handle_get_power_back('lunch')
                self.handle_get_power_back('dinner')
                continue
            else:
                logger.info(f"Now time is {current_hour} h,no need get power")
                break


    def handle_get_power_back(self, state='lunch', need_get_back=False):
        #
        if state == 'lunch' and self.appear(LUNCH_GETBACK):
            logger.info("Still have unclaimed lunch stamina")
            if need_get_back and self.device.click(LUNCH_GETBACK):
                logger.info("Use tongbao to exchange lunch stamina")
            return True
        if state == 'dinner' and self.appear(DINNER_GETBACK):
            logger.info("Still have unclaimed lunch stamina")
            if need_get_back and self.device.click(DINNER_GETBACK):
                logger.info("Use tongbao to exchange lunch stamina")
            return True
        return False
