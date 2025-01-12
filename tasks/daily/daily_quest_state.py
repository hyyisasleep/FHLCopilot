from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.page import page_daily_quest

from tasks.base.ui import UI
from tasks.daily.assets.assets_daily_reward import *



class DailyLivenessOCR(Digit):
    pass

class DailyQuestUI(UI):
    claimed_point_reward = False
    def _no_reward_to_get(self):
        return (
                (self.appear(ACTIVE_POINTS_1_LOCKED) or self.appear(ACTIVE_POINTS_1_CHECKED))
                and (self.appear(ACTIVE_POINTS_2_LOCKED) or self.appear(ACTIVE_POINTS_2_CHECKED))
                and (self.appear(ACTIVE_POINTS_3_LOCKED) or self.appear(ACTIVE_POINTS_3_CHECKED))
                and (self.appear(ACTIVE_POINTS_4_LOCKED) or self.appear(ACTIVE_POINTS_4_CHECKED))
                and (self.appear(ACTIVE_POINTS_5_LOCKED) or self.appear(ACTIVE_POINTS_5_CHECKED))
        )

    def _all_reward_got(self):
        return self.appear(ACTIVE_POINTS_5_CHECKED)


    def _get_liveness_point(self)->int:
        """
         get current point and write stored
        """
        # self.ui_ensure(page_daily_quest)
        point = 0
        for progress, button in zip(
                [20, 40, 60, 80, 100],
                [
                    ACTIVE_POINTS_1_LOCKED,
                    ACTIVE_POINTS_2_LOCKED,
                    ACTIVE_POINTS_3_LOCKED,
                    ACTIVE_POINTS_4_LOCKED,
                    ACTIVE_POINTS_5_LOCKED
                ]
        ):
            if self.appear(button):
                point = progress

        actual_point_ocr = Digit(OCR_DAILY_LIVENESS, lang=self.config.LANG)
        actual_point = actual_point_ocr.ocr_single_line(self.device.image)
        # retry, ocr sometimes error?
        # point(reward) < actual point <= 100
        if actual_point > 100 or actual_point < point:
            interval = Timer(1).start()
            cnt = 0
            while True:
                if cnt > 5:
                    logger.warning(f"OCR Failed after retrying 5 times, assume liveness is {point}")
                    # 还是识别不出来，将错就错吧拿奖励档当实际活跃度
                    if actual_point < point:
                        actual_point = point
                    break
                if interval.reached():
                    self.device.screenshot()
                    actual_point = actual_point_ocr.ocr_single_line(self.device.image)
                    interval.reset()
                    cnt += 1
                    if point <= actual_point <= 100:
                        break

        logger.attr('Daily Liveness', actual_point)

        self.config.stored.DailyLiveness.set(actual_point)
        return actual_point

    def get_active_point_reward(self, skip_first_screenshot=True):
        """
        self.claimed_point_reward will be set if claimed any point reward

        Returns:
            bool: If claimed any reward, self.claimed_point_reward
        """

        def get_active():
            for b in [
                ACTIVE_POINTS_1_UNLOCK,
                ACTIVE_POINTS_2_UNLOCK,
                ACTIVE_POINTS_3_UNLOCK,
                ACTIVE_POINTS_4_UNLOCK,
                ACTIVE_POINTS_5_UNLOCK
            ]:
                # Black gift icon
                # if self.image_color_count(b, color=(61, 53, 53), threshold=221, count=100):
                #     return b
                if self.appear(b):
                    return b
            return None
        self.ui_ensure(page_daily_quest)

        if not self.check_arrive_active_sub_page():
            return False



        interval = Timer(2)
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            # Check page_guide to wait until reward popup disappeared
            if self._no_reward_to_get():
                logger.info('No more reward to get')
                break
            if self.handle_reward():
                continue
            if interval.reached():
                if active := get_active():
                    self.device.click(active)
                    self.claimed_point_reward = True
                    interval.reset()

        # get current point and write stored
        self._get_liveness_point()

        return self.claimed_point_reward


    def check_arrive_active_sub_page(self,skip_first_screenshot=True):
        timeout = Timer(10).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if self.appear(ACTIVE_PAGE_CHECK):
                logger.info("Arrive active sub page")
                return True
            if timeout.reached():
                logger.warning("Can't switch to active sub page, break")
                return False
            if self.appear_then_click(GOTO_ACTIVE_PAGE):
                continue


        return False