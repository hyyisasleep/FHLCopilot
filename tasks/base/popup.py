
from typing import Callable

from module.base.base import ModuleBase
import numpy as np

from module.base.timer import Timer
from module.base.utils import get_color
from module.exception import RequestHumanTakeover
from module.logger import logger
from tasks.base.assets.assets_base_page import BACK  # , CLOSE
from tasks.base.assets.assets_base_popup import *


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



    def close_buy_details_popup(self,skip_first_screenshot=True):
        """
        Close goods details, used in shop and shapanlunyi,and use background from dark to light to check popup is close
        """
        timeout = Timer(10).start()
        clicked = False
        prev = np.mean(get_color(self.device.image, CLOSE_GOODS_DETAILS_BACKGROUND.area))
        # print(prev)
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get close buy details timeout,please check")
                return False

            if clicked:
                cur = np.mean(get_color(self.device.image, CLOSE_GOODS_DETAILS_BACKGROUND.area))
                if cur - prev > 30:
                    logger.info("Get color change, suggest popup is close")
                    self.interval_reset(CLOSE_GOODS_DETAILS)
                    return True


            if self.appear_then_click(CLOSE_GOODS_DETAILS):
                clicked = True

                continue
        return False

    def handle_week_jinge(self,interval=5) -> bool:
        if self.appear_then_click(SKIP_LAST_WEEK_LEVEL):
            logger.info("Skip last week level settlement page")
            return True
        if self.appear_then_click(SKIP_LAST_WEEK_LEVEL_2):
            logger.info("Skip last week level inherit page")
            return True
        return False

    # def handle_jingezhizun_rewards(self) -> bool:
    #     if self.appear_then_click(CLOSE_JINGEZHIZUN_REWARD):
    #         logger.info("Close jingezhizun rewards page, this first appear in 11.11-11.13")
    #         return True
    #     return False
    def drag_button(self,button:ButtonWrapper,direction="down"):
        """
        根据截图范围划拉，来自draggablelist算法
        """
        from numpy import random
        from module.base.utils import area_size, random_rectangle_vector_opted
        vector = (0.9, 0.9)
        vector = random.uniform(*vector)
        width, height = area_size(button.button)
        if direction == "down":
            vector = (0, vector * height)  # 不是说好的往下滑是带负号的呢
        elif direction == "up":
            vector = (0, -vector * height)
        # 左和右没用上。。。放着吧
        elif direction == "right":
            vector = (vector * width,0)
        else:
            vector = (-vector * width,0)
        p1, p2 = random_rectangle_vector_opted(vector, box=button.button)
        self.device.drag(p1, p2)

    def handle_taoyuan_blessing(self,interval=5) -> bool:
        """
        Popup blessing in taoyuanju everyday

        Args:
            interval:

        Returns:
            If handled.
        """
        if self.appear(TAOYUAN_GET_BLESSING,interval):

            self.drag_button(TAOYUAN_GET_BLESSING)
            return True
        if self.appear_then_click(TAOYUAN_GET_BLESSING_CONFIRM,interval):
            logger.info("Get blessing")
            return True
        return False

    def handle_cattery_get_cat(self, interval=5) -> bool:
        """
        Popup new cat

        Args:
            interval:

        Returns:
            If handled.
        """
        # 有时候会冒出一些标准猫让你捏脸，但是随机和完成键是同时出现的，避免抽风直接不随机了
        if self.appear_then_click(CATTERY_SHAPE_CAT_CONFIRM, interval):
            logger.info("Skip shape the cat")
            return True
        if self.appear_then_long_click(CATTERY_GET_CAT, interval):
            logger.info('Get a new cat')
            return True
        if self.appear_then_click(CATTERY_GET_CAT_QUIT, interval):
            return True
        return False

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

    def handle_begging_thanks(self,interval=5):

        if self.appear_then_click(CLUB_BEGGING_THANKS_CHECK,interval):
            logger.info("Give thanks to someone gave you fragments")
            return True

        if self.appear_then_click(CLUB_BEGGING_THANKS_CLOSE,interval):
            logger.info("Close thanks page")
            return True

    def handle_open_item_pack(self,interval=5):
        if self.appear_then_click(OPEN_ITEM_PACK,interval):
            return True