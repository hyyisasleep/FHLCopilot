from module.base.timer import Timer
from module.logger import logger

from tasks.base.page import page_guild, page_guild_begging
from tasks.base.ui import UI
from tasks.guild.assets.assets_guild import *

class Guild(UI):
    """
    雅社：
    签到 fin
    放河灯
    做悬赏
    周五紫薇布阵
    其他活动提醒，比如沙盘比如预卜

    """

    def run(self):
        """
        """
        logger.hr('Guild sign in', level=1)
        # 跳转到互动界面
        self.ui_ensure(page_guild)

        if self._check_join_guild():
            self._sign_in()
            self._float_river_lantern()
        self.ui_goto_main()



        self.config.task_delay(server_update=True)

    def _sign_in(self,skip_first_screenshot=True,interval=2):
        timeout = Timer(15).start()

        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.info("Get goto sign in page timeout")
                break
            if self.appear_then_click(NOTICE_CHECK):
                logger.info("Close notice")
                continue
            if self.appear_then_click(GOTO_SIGN_IN,interval=2):
                continue
            if self.handle_reward():
                continue
            if self.appear(SIGN_IN_PAGE_CHECK):
                if self.appear_then_click(SIGN_IN_UNLOCK, interval):
                    logger.info("Sign in free")
                    continue
                if self.appear(SIGN_IN_LOCKED, interval):
                    logger.info("Sign in finish")
                    break
        # 返回界面，单开一个循环吧要不
        skip_first_screenshot = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if self.ui_page_appear(page_guild):
                logger.info("Successful return to guild page")
                break
            if self.appear_then_click(SIGN_IN_PAGE_CLOSE):
                logger.info("Close sign in page")
                continue
    # 判断有没有加入雅社
    def _check_join_guild(self)->bool:
        timeout=Timer(5,count=3).start()
        while 1:
            self.device.screenshot()
            if timeout.reached():
                logger.info("Get timeout, assume user join guild")
                return True
            if self.appear(NOT_JOIN_GUILD_CHECK):
                logger.info("User didn't join guild, stop run guild task")
                return False
            if self.appear(GOTO_SIGN_IN) or self.appear(NOTICE_CHECK):
                logger.info("Check finish, user join guild")
                return True

    def _float_river_lantern(self):
        self.ui_ensure(page_guild_begging)



        skip_first_screenshot = True
        timeout = Timer(15).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if self.appear(BEGGING_LOCKED):
                logger.info("Begging finish")
                break
            if timeout.reached():
                logger.warning("Get put lantern timeout")
                break
            # 有时候感谢会在判定已经进入河灯界面之后再出。。服啦
            if self.handle_begging_thanks():
                timeout.reset()
                continue
            if self.appear_then_click(BEGGING_UNLOCK):
                continue
            if self.appear_then_click(BEGGING_PUT_LANTERN_1):
                logger.info("Put guild lantern")
                continue
            if self.appear_then_click(BEGGING_PUT_LANTERN_2):
                logger.info("Put friend lantern")
                continue
            if self.appear_then_click(BEGGING_PUT_LANTERN_CONFIRM):
                continue


        self.ui_ensure(page_guild)

        pass


if __name__ == '__main__':
    ui = Guild('fhlc')
    ui.device.screenshot()
    ui.run()
    # ui.image_file = r'C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20241118-171812.png'
    # print(ui.appear(CLUB_BEGGING_THANKS_CLOSE))