from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_interact
from tasks.base.ui import UI
from tasks.dispatch.assets.assets_dispatch_interact import *

#TODO: 送礼中途升级
# TODO: 怎么判断结束。。。。
class Interact(UI):

    def run(self):
        """
        """
        logger.hr('Give celebrity gift', level=1)
        # 跳转到互动界面
        self.ui_ensure(page_interact)
        finish = self._give_gift()
        if finish:
            self.config.stored.CelebrityInteract.set(finish)
        self.ui_goto_main()



        # self.config.task_delay(server_update=True)

    def _give_gift(self, interval=2, skip_first_screenshot=True):

        timeout = Timer(10).start()
        finish = 0
        show = False
        # skip_first_screenshot = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.info("Get interact timeout")
                break
            if self.appear_then_click(LEVEL_UP_NOTICE):
                logger.info("Close level up popup")
                continue
            if self.appear_then_click(LEVEL_REWARD_UNLOCK):
                logger.info("Get friendship upgrade reward")
                continue
            if self.appear(GIVE_GIFT_CHECK):
                if not show:
                    logger.info("Today has fragment to get")
                    show = True
                if self.appear_then_click(GIVE_MODE_UPGRADE_UNLOCK, interval):
                    logger.info("Choose mode: give gift until friendship upgrade")
                    continue
                if self.appear(GIVE_MODE_UPGRADE_LOCKED, interval):
                    self.appear_then_click(GIVE_GIFT, interval)
                    logger.info("Give gift to celebrity")
                    finish = 1
                    continue
            if self.handle_reward(interval):
                logger.info("Get fragment reward or upgrade reward")
                continue
        return finish

if __name__ == "__main__":
    ui = Interact("fhlc")
    # ui.image_file = r'C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20250107-142723.png'
    # print(ui.appear(GIVE_MODE_UPGRADE_UNLOCK))
    # ui.image_file = r'C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20250107-142739.png'
    # print(ui.appear(GIVE_MODE_UPGRADE_UNLOCK))