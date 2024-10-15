from typing import Callable



from module.base.base import ModuleBase

from module.logger import logger
from tasks.PVP.assets.assets_pvp_JinGeYanWu import SKIP_LAST_WEEK_LEVEL, SKIP_LAST_WEEK_LEVEL_2
# tasks.PVP.assets.assets_PVP_JinGeYanWu import SKIP_LAST_WEEK_LEVEL_2, SKIP_LAST_WEEK_LEVEL
from tasks.base.assets.assets_base_page import BACK, CLOSE_UPDATE_NOTICE  # , CLOSE
from tasks.base.assets.assets_base_popup import *
# from tasks.taoyuanju.assets.assets_taoyuanju import GET_BLESSING, GET_BLESSING_CONFIRM


# 解决弹出窗口？

class PopupHandler(ModuleBase):
    def reward_appear(self) -> bool:
        # 不知道为什么只有一张图的情况调这个api会报错- -
        return self.appear(GET_REWARD)
        # for button in GET_REWARD.buttons:
        #     image = self.image_crop(button.search, copy=False)
        #     image = color_similarity_2d(image, color=(203, 181, 132))
        #     if button.match_template(image, direct_match=True):
        #         return True
        # return False

    def handle_reward(self, interval=5, click_button: ButtonWrapper = None) -> bool:
        """
        Args:
            interval:
            click_button: Set a button to click

        Returns:
            If handled.
        """
        # Same as ModuleBase.match_template()
        self.device.stuck_record_add(GET_REWARD)

        if interval and not self.interval_is_reached(GET_REWARD, interval=interval):
            return False

        #appear = self.reward_appear()
        appear = self.appear(GET_REWARD)
        if click_button is None:
            if appear:
                self.device.click(GET_REWARD)
        else:
            if appear:
                logger.info(f'{GET_REWARD} -> {click_button}')
                self.device.click(click_button)

        if appear and interval:
            self.interval_reset(GET_REWARD, interval=interval)

        return appear

    def handle_week_jinge(self,interval=5) -> bool:
        if self.appear_then_click(SKIP_LAST_WEEK_LEVEL):
            logger.info("Skip last week level settlement page")
            return True
        if self.appear_then_click(SKIP_LAST_WEEK_LEVEL_2):
            logger.info("Skip last week level inherit page")
            return True
        return False
    def handle_taoyuan_blessing(self,interval=5) -> bool:
        """
        Popup blessing in taoyuanju everyday

        Args:
            interval:

        Returns:
            If handled.
        """
        if self.appear(TAOYUAN_GET_BLESSING,interval):
            # 抄的draggablelist算法
            from numpy import random
            from module.base.utils import area_size, random_rectangle_vector_opted
            vector = (0.9, 0.5)
            vector = random.uniform(*vector)
            width, height = area_size(TAOYUAN_GET_BLESSING.button)
            vector = (0, vector * height)  # 不是说好的往下滑是带负号的呢
            p1, p2 = random_rectangle_vector_opted(vector, box=TAOYUAN_GET_BLESSING.button)
            self.device.drag(p1, p2)
            return True
        if self.appear_then_click(TAOYUAN_GET_BLESSING_CONFIRM,interval):
            logger.info("Get blessing")
            return True
        return False

    def handle_cattery_get_cat(self, interval=5) -> bool:
        """
        Popup blessing in taoyuanju everyday

        Args:
            interval:

        Returns:
            If handled.
        """
        if self.appear_then_long_click(CATTERY_GET_CAT, interval):
            logger.info('Get a new cat')
            return True
        if self.appear_then_click(CATTERY_GET_CAT_QUIT, interval):
            return True
        return False
    # def handle_battle_pass_notification(self, interval=5) -> bool:
    #     """
    #     Popup notification that you enter battle pass the first time.
    #
    #     Args:
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if self.appear_then_click(BATTLE_PASS_NOTIFICATION, interval=interval):
    #         return True
    #
    #     return False

    # def handle_monthly_card_reward(self, interval=1) -> bool:
    #     """
    #     Popup at 04:00 server time if you have purchased the monthly card.
    #
    #     Args:
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if self.appear_then_click(MONTHLY_CARD_REWARD, interval=interval):
    #         # Language check at the first login of the day may fail due to popups
    #         # Retry later
    #         from tasks.base.main_page import MainPage
    #         if not MainPage._lang_check_success:
    #             MainPage._lang_checked = False
    #         return True
    #     if self.appear_then_click(MONTHLY_CARD_GET_ITEM, interval=interval):
    #         from tasks.base.main_page import MainPage
    #         if not MainPage._lang_check_success:
    #             MainPage._lang_checked = False
    #         return True
    #
    #     return False

    # def handle_popup_cancel(self, interval=2) -> bool:
    #     """
    #     Args:
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if self.appear_then_click(POPUP_CANCEL, interval=interval):
    #         return True
    #
    #     return False
    #
    # def handle_popup_confirm(self, interval=2) -> bool:
    #     """
    #     Args:
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if self.appear_then_click(POPUP_CONFIRM, interval=interval):
    #         return True
    #
    #     return False
    #
    # def handle_popup_single(self, interval=2) -> bool:
    #     """
    #     Popup with one single confirm button in the middle.
    #
    #     Args:
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if self.appear_then_click(POPUP_SINGLE, interval=interval):
    #         return True
    #
    #     return False

    # def handle_get_light_cone(self, interval=2) -> bool:
    #     """
    #     Popup when getting a light cone from Echo of War.
    #
    #     Args:
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if self.appear(GET_LIGHT_CONE, interval=interval):
    #         logger.info(f'{GET_LIGHT_CONE} -> {GET_REWARD}')
    #         self.device.click(GET_REWARD)
    #         return True
    #
    #     return False

    # def handle_get_character(self, interval=2) -> bool:
    #     """
    #     Popup when getting a character from rogue rewards.
    #
    #     Args:
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if self.appear(GET_CHARACTER, interval=interval):
    #         logger.info(f'{GET_CHARACTER} -> {GET_REWARD}')
    #         self.device.click(GET_REWARD)
    #         return True
    #
    #     return False

    # def handle_ui_close(self, appear_button: ButtonWrapper | Callable, interval=2) -> bool:
    #     """
    #     Args:
    #         appear_button: Click if button appears
    #         interval:
    #
    #     Returns:
    #         If handled.
    #     """
    #     if callable(appear_button):
    #         if self.interval_is_reached(appear_button, interval=interval) and appear_button():
    #             logger.info(f'{appear_button.__name__} -> {CLOSE}')
    #             self.device.click(CLOSE)
    #             self.interval_reset(appear_button, interval=interval)
    #             return True
    #     else:
    #         if self.appear(appear_button, interval=interval):
    #             logger.info(f'{appear_button} -> {CLOSE}')
    #             self.device.click(CLOSE)
    #             return True
    #
    #     return False

    def handle_promote_pack(self):
        if self.appear_then_click(CLOSE_PROMOTE_PACK):
            return True
        return False
    def handle_ui_back(self, appear_button: ButtonWrapper | Callable, interval=2) -> bool:
        """
        Args:
            appear_button: Click if button appears
            interval:

        Returns:
            If handled.
        """
        if callable(appear_button):
            if self.interval_is_reached(appear_button, interval=interval) and appear_button():
                logger.info(f'{appear_button.__name__} -> {BACK}')
                self.device.click(BACK)
                self.interval_reset(appear_button, interval=interval)
                return True
        else:
            if self.appear(appear_button, interval=interval):
                logger.info(f'{appear_button} -> {BACK}')
                self.device.click(BACK)
                return True

        return False
