from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_shop
# from module.ocr.ocr import Digit
from tasks.shop.assets.assets_shop import *
# from tasks.base.page import page_shop
from tasks.base.ui import UI


class DailyShop(UI):

    def run(self):
        """

        """
        logger.hr('Buy daily shop gift', level=1)
        # self.device.screenshot()
        self.device.screenshot()
        self.ui_goto_main()
        self.get_friendship_point()
        self.ui_ensure(page_shop)

        self.buy_gift(mode='copper-puppet')

        self.buy_gift(mode='sign-in')

        self.buy_gift(mode='monthly-card')

        self.buy_gift(mode='leisure-friendship')

        self.buy_gift(mode='leisure-cattery')

        self.ui_goto_main()
        self.config.task_delay(server_update=True)

    def handle_gift_mode(self, mode, interval=5):
        if mode == 'sign-in':
            if self.appear(MENU_GIFT_DAILY_CHECK):
                if self.appear_then_click(MENU_GIFT_DAILY_SIGN_IN_PACK_UNLOCK):
                    logger.info("Buy daily sign in gift")
                    return True
            if self.appear_then_click(MENU_GIFT_GOTO_DAILY):
                return True
            if self.appear_then_click(MENU_GOTO_GIFT):
                return True
        elif mode == 'monthly-card':
            # if self.appear(MENU_MONTHLY_CARD_CHECK):
            if self.appear_then_click(MONTHLY_CARD_30_UNLOCK):
                logger.info("Get 30 monthly card")
                return True
            if self.appear_then_click(MONTHLY_CARD_68_UNLOCK):
                logger.info("Get 68 monthly card")
                return True
            if self.appear_then_click(MENU_GOTO_MONTHLY_CARD):
                return True
        elif mode == 'leisure-friendship':

            # TODO: 加检测已领取 有时候在奖励界面点68月卡，算进奖励然后就返回了
            if self.handle_choose_gift_num():
                return True
            if self.appear(MENU_LEISURE_FRIENDSHIP_CHECK):
                if self.appear_then_click(LEISURE_FRIENDSHIP_GIFT_UNLOCK):
                    return True
            if self.appear_then_click(MENU_LEISURE_GOTO_FRIENDSHIP):
                return True
            if self.appear_then_click(MENU_GOTO_LEISURE):
                return True
        elif mode == 'leisure-cattery':
            if self.handle_choose_gift_num():
                return True
            if self.appear(MENU_LEISURE_CATTERY_CHECK):
                if self.appear_then_click(LEISURE_CATTERY_TOY_UNLOCK):
                    return True
                if self.appear_then_click(LEISURE_CATTERY_FRAGMENT_UNLOCK):
                    return True
            if self.appear_then_click(MENU_LEISURE_GOTO_CATTERY):
                return True
            if self.appear_then_click(MENU_GOTO_LEISURE):
                return True
        elif mode == 'copper-puppet':
            if self.handle_choose_gift_num():
                return True
            if self.appear(MENU_RESOURCE_COPPER_CHECK):
                if self.appear_then_click(MENU_RESOURCE_COMMON_CAT_PUPPET_UNLOCK):
                    logger.info("Buy 3 common cat puppet in copper menu")
                    return True
            if self.appear_then_click(MENU_RESOURCE_GOTO_COPPER):
                return True
            if self.appear_then_click(MENU_GOTO_RESOURCE):
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

    def get_friendship_point(self, skip_first_screenshot=True):
        timeout = Timer(4).start()
        finish = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.info("Get friendship point timeout")
                break

            if finish:
                # 关不掉不重复啊啊啊啊 不对又没法退循环了
                self.appear_then_click(CLOSE_FRIEND_PAGE)
                # timeout.reset()
                continue

            if self.appear_then_click(GIVE_RECEIVE_FRIENDSHIP_POINT):
                logger.info("Give and receive friend ship point")
                timeout.reset()
                finish = True
                continue
            if self.appear_then_click(GOTO_FRIEND_PAGE):
                logger.info("Open friend page")
                continue


if __name__ == '__main__':
    ui = DailyShop('fhlc')
    ui.device.screenshot()
    # print(ui.is_in_main())
    ui.run()
    # ui.image_file = r"C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20240908-190406.png"
    # print(ui.pvp_ocr())
