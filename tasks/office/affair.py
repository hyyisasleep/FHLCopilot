from module.base.timer import Timer
from module.logger import logger
# from tasks.base.assets.assets_base_page import CLOSE_LOGIN_ADVERTISEMENT
from tasks.base.assets.assets_base_popup import GET_REWARD
from tasks.base.page import page_office_affair, page_office
from tasks.base.ui import UI
from tasks.office.assets.assets_office_affair import *


class Affair(UI):

    def run(self, skip_first_screenshot=True):
        """

        """
        logger.hr('Deal with taoyuan affair', level=1)
        self.ui_ensure(page_office_affair, skip_first_screenshot)
        has_reward = self._deal_with_affairs()
        #
        # if has_reward:
        #     # logger.info("Has impression reward to get")
        #     self._get_affairs_impression_reward()
        self.ui_ensure(page_office)

        self.config.task_delay(server_update=True)

    def _deal_with_affairs(self, interval=2, skip_first_screenshot=True) -> bool:
        """
        # 喜报 经过测试发现就算没奖励也会把AFFAIR_HAS_REWARD的红点识别成有奖励
        # 所以这个函数只会返回True
        """
        timeout = Timer(10).start()
        start_deal = False
        affair_cnt = 0
        has_reward = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.info("Get taoyuan affair timeout")
                break

            # if not has_reward and self.appear(AFFAIR_HAS_REWARD):
            #     has_reward = True
            # ocr_affair = Digit(DEAL_WITH_AFFAIR_START)
            # num = ocr_affair.ocr_single_line(self.device.image)
            # 显示事务0，不用做
            if self.appear(DEAL_WITH_AFFAIR_FINISH, interval):
                if start_deal:
                    logger.info("Finish deal with affair")
                    break
                else:
                    logger.info("No need deal with affair")
                    break
            if not start_deal and self.appear_then_click(DEAL_WITH_AFFAIR_START, interval):
                logger.info("Start deal with affair")
                start_deal = True
                continue
            # 1已经选过了就点2
            if self.appear_then_click(CHOOSE_AFFAIR_1, interval):
                # start_deal = True
                affair_cnt += 1
                logger.info(f"Finish {affair_cnt} affair")
                timeout.reset()
                continue
            if self.appear_then_click(CHOOSE_AFFAIR_2, interval):
                affair_cnt += 1
                logger.info(f"Finish {affair_cnt} affair with choice 2")
                timeout.reset()
                continue
            # 只写handle_reward每次点完事务都要点一次领奖？怪了
            if self.appear(GET_REWARD, interval):
                self.handle_reward()
                timeout.reset()
                continue

        return has_reward

    def _get_affairs_impression_reward(self, interval=2, skip_first_screenshot=True):
        """
        TODO:没测完先把机会用完了

        """
        timeout = Timer(10).start()
        get_reward_finish = True

        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.info("Get taoyuan affair reward timeout")
                break

            if get_reward_finish and self.appear(AFFAIR_HAS_REWARD):
                get_reward_finish = False
                self.appear_then_click(AFFAIR_GOTO_TODO)
                self.appear_then_click(AFFAIR_GOTO_IMPRESSION)
                logger.info("Switch page to refresh reward's location")
                # timeout.reset()
                continue
            if get_reward_finish:
                logger.info("Get impression reward finish")
                # timeout.reset()
                break
            if self.appear_then_click(AFFAIR_GOTO_IMPRESSION):
                timeout.reset()
                continue
            if self.appear_then_click(REWARD_UNLOCK):
                continue
            if self.handle_reward():
                continue
            if self.appear_then_click(GET_REWARD_UNLOCK):
                continue
            if self.appear_then_click(CLOSE_REWARD_PAGE):
                timeout.reset()
                continue
            if self.appear(REWARD_FINISH):
                get_reward_finish = True
                continue


if __name__ == '__main__':
    ui = Affair('fhlc')
    # ui.image_file = r'C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20241012-203428.png'
    # print(ui.appear(AFFAIR_HAS_REWARD))
    ui.device.screenshot()
    ui.run()
