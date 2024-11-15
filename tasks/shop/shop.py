from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_shop

from tasks.shop.assets.assets_shop import *
from tasks.shop.assets.assets_shop_goods import *
from tasks.shop.assets.assets_shop_monthly_card import *

# from tasks.base.ui import UI
# from tasks.shop.assets.assets_shop_ui import *
from tasks.shop.ui import ShopUI, TAB_STATE_MONTHLY_CARD, SUB_TAB_STATE_GIFT_DAILY, SUB_TAB_STATE_LEISURE_FRIENDSHIP, \
    SUB_TAB_STATE_LEISURE_CATTERY, SUB_TAB_STATE_RESOURCE_COPPER


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

        # self.buy_gift(mode='copper-puppet')
        #
        # self.buy_gift(mode='sign-in')
        #
        #
        #
        # # self.buy_gift(mode='monthly-card')
        #
        # self.buy_gift(mode='leisure-friendship')
        #
        # self.buy_gift(mode='leisure-cattery')

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

    def handle_gift_mode(self, mode, interval=5):
        if mode == SUB_TAB_STATE_GIFT_DAILY:
            if self.appear_then_click(MENU_GIFT_DAILY_SIGN_IN_PACK):
                logger.info("Buy daily sign in gift")
                return True

        elif mode == SUB_TAB_STATE_LEISURE_FRIENDSHIP:

            # TODO: 加检测已领取 有时候在奖励界面点68月卡，算进奖励然后就返回了
            if self.handle_choose_gift_num():
                return True
            if self.appear_then_click(LEISURE_FRIENDSHIP_GIFT):
                return True

        elif mode == SUB_TAB_STATE_LEISURE_CATTERY:
            if self.handle_choose_gift_num():
                return True
            if self.appear_then_click(LEISURE_CATTERY_TOY):
                return True
            if self.appear_then_click(LEISURE_CATTERY_FRAGMENT):
                return True

        elif mode == SUB_TAB_STATE_RESOURCE_COPPER :
            if self.handle_choose_gift_num():
                return True
            if self.appear_then_click(MENU_RESOURCE_COMMON_CAT_PUPPET):
                logger.info("Buy 3 common cat puppet in copper menu")
                return True

        return False

    def handle_choose_gift_num(self):
        if self.appear_then_click(BUY_GIFT_MAX_LOCK):
            logger.info("Buy max gift")
            return True
        if self.appear_then_click(BUY_GIFT_MAX_UNLOCK):
            return True
        return False

    def buy_gift(self, mode, interval=2, skip_first_screenshot=True):
        timeout = Timer(5).start()
        # 跳转到商品对应菜单
        self.shop_sub_tab_goto(mode)
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.info(f"Get buy {mode} gift timeout")
                break
            if self.handle_reward():
                continue
            if self.handle_gift_mode(mode, interval):
                timeout.reset()
                continue


if __name__ == '__main__':
    ui = DailyShop('fhlc')
    # ui.device.screenshot()
    # # print(ui.is_in_main())
    # ui.run()
    # ui.image_file = r"C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20241015-132802.png"
    # print(ui.appear(MENU_RESOURCE_COMMON_CAT_PUPPET))

