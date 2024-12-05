from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_shop


from tasks.shop.assets.assets_shop_goods import *
from tasks.shop.assets.assets_shop_monthly_card import *


from tasks.shop.ui import ShopUI, TAB_STATE_MONTHLY_CARD


class DailyShop(ShopUI):

    def run(self):
        """

        """
        logger.hr('Buy daily shop gift', level=1)
        # self.device.screenshot()
        self.device.screenshot()
        self.ui_goto_main()

        self.ui_ensure(page_shop)

        self.get_monthly_card()

        self.buy_goods(GIFT_DAILY_GOODS_SIGN_IN_PACK)

        self.buy_goods(RESOURCE_COPPER_GOODS_COMMON_CAT_PUPPET)
        self.buy_goods(LEISURE_CATTERY_GOODS_FRAGMENT)
        self.buy_goods(LEISURE_FRIENDSHIP_GOODS_GIFT)

        self.buy_goods(LEISURE_CATTERY_GOODS_TOY)



        self.ui_goto_main()
        self.config.task_delay(server_update=True)

    def get_monthly_card(self, skip_first_screenshot=True):
        # TODO: 在配置里加是否拥有大小月卡
        # 用switch Tab GOTO？
        timeout = Timer(10).start()
        # 检测小月卡
        self.shop_tab_goto(TAB_STATE_MONTHLY_CARD)
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get monthly card(30) timeout")
                break
            if self.appear(NOT_BUY_MONTHLY_CARD_30_CHECK):
                logger.info("User didn't buy monthly card(30), or expired")
                # TODO: update config
                break
            if self.appear(MONTHLY_CARD_30_LOCKED):
                logger.info("Get monthly card(30) finish")
                break
            if self.handle_reward():
                logger.info("Get monthly card(30) reward")
                continue
            if self.appear_then_click(MONTHLY_CARD_30_UNLOCK):
                continue

        timeout.reset()

        # 检测大月卡
        while 1:

            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get monthly card(68) timeout")
                break
            if self.appear(NOT_BUY_MONTHLY_CARD_68_CHECK):
                logger.info("User didn't buy 68's monthly card, or expired")
                # TODO: update config
                break
            if self.appear(MONTHLY_CARD_68_LOCKED):
                logger.info("Finish")
                break
            if self.handle_reward():
                logger.info("Get monthly card(68) reward")
                continue
            if self.appear_then_click(MONTHLY_CARD_68_UNLOCK):
                logger.info("Get 68 monthly card")
                continue



if __name__ == "__main__":
    ui = DailyShop("fhlc")
    ui.run()