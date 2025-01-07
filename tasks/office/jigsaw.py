from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_office_jigsaw, page_office
from tasks.base.ui import UI
from tasks.office.assets.assets_office_jigsaw import *



class Jigsaw(UI):

    def run(self, skip_first_screenshot=True):
        self.ui_ensure(page_office_jigsaw)
        logger.hr('Convert baigongtu', level=1)
        self.ui_ensure(page_office_jigsaw, skip_first_screenshot)
        if self._goto_convert_page():
            self._convert_kaogong()
        self.ui_ensure(page_office)

        # self.config.task_delay(server_update=True)

    def _goto_convert_page(self, skip_first_screenshot=True) -> int:
        # skip_first_screenshot = False
        timeout = Timer(1).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.info("No need convert baigongtu")
                return False
            if self.appear(CONVERT_CHECK):
                return True
            if self.appear_then_click(GOTO_CONVERT):
                logger.info("Go to convert ticket")
                continue


    def _convert_kaogong(self):

        # 直接拉到10
        # 但是好像不好用？
        # self._item_amount_set(10, BAIGONGTU_AMOUNT_OCR, BAIGONGTU_AMOUNT_MINUS, BAIGONGTU_AMOUNT_PLUS)

        timeout = Timer(5).start()
        skip_first_screenshot = False

        finish = False
        amount = 0
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if finish and self.appear(CONVERT_FINISH_PAGE_CHECK):
                logger.info("Convert finish")
                break

            if timeout.reached():
                logger.info("Get confirm to convert bgt timeout")
                break

            if self.appear(CONVERT_CONFIRM_LOCKED):
                self.appear_then_click(CONVERT_CLOSE)
                finish = True
                timeout.reset()
                continue

            if self.appear(ITEM_AMOUNT_MAX):
                self.appear_then_click(CONVERT_CONFIRM)
                # logger.info(f"Convert {amount} item")
                continue

            if self.appear_then_click(ITEM_AMOUNT_PLUS, interval=0.5):
                logger.info("add a item")
                amount += 1
                timeout.reset()
                continue

            if self.handle_reward():
                timeout.reset()
                continue

            if self.appear(CONVERT_CHECK):
                timeout.reset()
                continue


if __name__ == "__main__":
    ui = Jigsaw('fhlc')
    ui.device.screenshot()
    ui.run()