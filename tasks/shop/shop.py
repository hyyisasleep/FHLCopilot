from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.page import page_shop


from tasks.shop.assets.assets_shop_goods import *
from tasks.shop.assets.assets_shop_monthly_card import *


from tasks.shop.ui import ShopUI, TAB_STATE_MONTHLY_CARD


class MonthlyCardOCR(Digit):
    def after_process(self, result):
        # 今日已领取，剩余xx小时=明天过期
        if "小时" in result:
            return '0'
        else:
            return super().after_process(result)

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
        """
        领月卡+写配置
        不小心把大月卡价格记成68了哈哈算了懒得改了
        """
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

                break
            if self.appear(MONTHLY_CARD_30_LOCKED):
                logger.info("Get monthly card(30) finish")

                # OCR and update config
                mc30 = MonthlyCardOCR(OCR_BUY_MONTHLY_CARD_30)
                remain_days = mc30.ocr_single_line(self.device.image)
                self.config.stored.MonthlyCard30.value = remain_days
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
                logger.warning("Get monthly card(60) timeout")
                break
            if self.appear(NOT_BUY_MONTHLY_CARD_68_CHECK):
                logger.info("User didn't buy 60's monthly card, or expired")
                # TODO: update config
                break
            if self.appear(MONTHLY_CARD_68_LOCKED):
                logger.info("Finish")
                mc68 = MonthlyCardOCR(OCR_BUY_MONTHLY_CARD_68)
                remain_days = mc68.ocr_single_line(self.device.image)
                self.config.stored.MonthlyCard68.value = remain_days
                break
            if self.handle_reward():
                logger.info("Get monthly card(60) reward")
                continue
            if self.appear_then_click(MONTHLY_CARD_68_UNLOCK):
                logger.info("Get 60 monthly card")
                continue



if __name__ == "__main__":
    ui = DailyShop("fhlc")
    ui.device.screenshot()
    ui.run()