from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_main, page_moments

from tasks.base.ui import UI
from tasks.dispatch.assets.assets_dispatch import *
from tasks.dispatch.interact import Interact
from tasks.dispatch.moments import Moments


class Dispatch(UI):
    """
    首页忘川速办，小麒麟头
    之前写的是Kylin，但是查了一下dispatch有迅速办成的意思，好的就你了
    ---
    功能：
    领供台奖励、虾球
    名士送礼一天俩碎片（设置为领第一个
    雅社乞讨碎片
    体力放置？
    躲猫猫

    TODO: 一个draggablelist
    """

    def run(self):
        """
        """
        logger.hr('Kylin‘s dispatch', level=1)
        self.ui_ensure(page_main)


        # 送好友友情点
        self.get_friendship_point()

        # 打开麒麟头+领供台奖励+领虾球+关闭麒麟头
        self._kylin_affair()
        # 赠礼
        Interact(self.config, self.device).run()
        # 知交圈点赞三次
        Moments(self.config, self.device).run()
        self.config.task_delay(server_update=True)

    def _kylin_affair(self, skip_first_screenshot=True):
        """
        目前是把领虾球和供台奖励写了
        """
        timeout = Timer(10).start()
        finish = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.info("Get kylin affair timeout")
                break
            # 当它处理完了
            if finish and self.appear(GOTO_KYLIN_PAGE_NO_REWARD):
                logger.info("Close kylin affair page")
                break
            if not finish and self.appear_then_click(GOTO_KYLIN_PAGE):
                logger.info("Open kylin page")
                continue
            if self.handle_reward():
                continue
            if self.appear_then_click(CAT_ALTAR_UNLOCK,interval=2):
                logger.info("Get cat altar reward")
                timeout.reset()
                continue
            if self.appear_then_click(GET_SHRIMP_BALL_UNLOCK,interval=2):
                logger.info("Get shrimp ball")
                timeout.reset()
                continue
            if self.appear(CAT_ALTAR_LOCKED) and self.appear(GET_SHRIMP_BALL_LOCKED):
                # 有红点和没红点两种友情标
                if (self.appear_then_click(GOTO_FRIEND_PAGE)
                        or self.appear_then_click(GOTO_FRIEND_PAGE_NO_REWARD)):
                    timeout.reset()
                    logger.info("Close kylin affair page")
                    finish = True
                continue

    def get_friendship_point(self, skip_first_screenshot=True):
        timeout = Timer(5).start()
        finish = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                self.appear_then_click(CLOSE_FRIEND_PAGE, interval=2)
                logger.info("Get friendship point timeout")
                break

            # 关闭后会弹出麒麟头
            if finish and (self.appear(GOTO_KYLIN_PAGE) or self.appear(GOTO_KYLIN_PAGE_NO_REWARD)):
                logger.info("Close friendship page")
                break
            if finish:
                self.appear_then_click(CLOSE_FRIEND_PAGE, interval=2)
                # timeout.reset()
                continue
            if self.appear_then_click(GOTO_FRIEND_SUB_PAGE):
                logger.info("Has stranger's message,turn to friend page")
                continue
            if self.appear_then_click(GIVE_RECEIVE_FRIENDSHIP_POINT):
                logger.info("Give and receive friend ship point")
                timeout.reset()
                finish = True
                continue
            if self.appear_then_click(GOTO_FRIEND_PAGE):
                logger.info("Open friend page")
                timeout.reset()
                continue


if __name__ == "__main__":
    ui = Dispatch("fhlc")
    # ui.image_file = r'C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20241011-163153.png'
    # print(ui.appear(GOTO_KYLIN_PAGE_NO_REWARD))
    # print(ui.appear(GET_SHRIMP_BALL_LOCKED))
    ui.device.screenshot()
    ui.run()
