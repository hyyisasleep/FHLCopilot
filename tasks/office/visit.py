from module.base.timer import Timer
from module.logger import logger
# from tasks.base.assets.assets_base_page import BACK
from tasks.base.page import page_office_visit, page_office
from tasks.base.ui import UI
from tasks.office.assets.assets_office_visit import *


class Visit(UI):

    def run(self, skip_first_screenshot=True):
        """

        """
        logger.hr('Deal with taoyuan affair', level=1)
        self.ui_ensure(page_office_visit, skip_first_screenshot)
        self._visit_other()
        self.ui_ensure(page_office)

        # self.config.task_delay(server_update=True)

    def _visit_other(self, interval=2, skip_first_screenshot=True):

        retry = 0
        first_visit = False
        second_visit = False
        third_visit = False
        timeout = Timer(20).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.warning("Get visit other timeout")
                break
            if first_visit and second_visit and third_visit:
                break
            if retry > 3:
                logger.warning("Retry visit other times get 3, stop")
                break

            #TODO: 我草到了还在点啊！
            if self.appear_then_click(VISIT_GOTO_MY_VISIT_LIST):
                logger.info("Goto my visit list")
                # timeout.reset()
                continue
            if self.appear(MY_VISIT_LIST_CHECK):

                if not first_visit:
                    first_visit = self._click_like_in_other_office(VISIT_FIRST)
                    logger.info("Visit first office")
                    if not first_visit:
                        logger.info("Fail to visit first office")
                elif not second_visit:
                    logger.info("Visit second office")
                    second_visit = self._click_like_in_other_office(VISIT_SECOND)
                    # 要是出现超时的话重新尝试拜访一下，第二个拜访会在拜访列表里变为第一个
                    if not second_visit:
                        logger.info("Fail to visit second office,try again")
                        second_visit = True
                        first_visit = False
                        retry += 1
                elif not third_visit:
                    logger.info("Visit third office")
                    third_visit = self._click_like_in_other_office(VISIT_THIRD)
                    if not third_visit:
                        logger.info("Fail to visit third office,try again")
                        third_visit = True
                        first_visit = False
                        retry += 1
                timeout.reset()
                continue
        pass

    def _click_like_in_other_office(self, button, skip_first_screenshot=True) -> bool:
        finish = False
        timeout = Timer(15).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.handle_reward():
                logger.info("Get a flower")
                continue
            # 跳转到
            if self.appear(LIKE_LOCKED):
                logger.info("Give like finish or no need give like")
                finish = True
                break
            if timeout.reached():
                logger.info("Get timeout in other office page")
                break
            if self.appear(LIKE_GET_LIMIT):
                logger.warning("FHLC wrongly go to unknown one's office, sorry")
                finish = True
                break
            if self.appear_then_click(button,interval=2):
                logger.info("Turn to other office page")
                continue
            if self.appear_then_click(LIKE_UNLOCK,interval=2):
                logger.info("give a like")
                # timeout.reset()
                continue
        return finish






        self.ui_ensure(page_office_visit)
        return finish


# if __name__ == 'main':
# ui = Visit('fhlc')
# ui.device.screenshot()
# ui.run()