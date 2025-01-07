from module.base.timer import Timer
from module.config.utils import get_server_weekday
from module.logger import logger
from tasks.PVP.ShaPanLunYi import ShaPanLunYi

from tasks.base.page import page_guild, page_guild_begging

from tasks.guild.assets.assets_guild import *
from tasks.guild.cosplay import Cosplay
from tasks.guild.mission import GuildMission


class Guild(GuildMission):
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
        logger.hr('Guild', level=1)
        # 跳转到互动界面
        self.ui_ensure(page_guild)
        # 先确定有没有雅社
        if self._check_join_guild():

            # 重置昨天的悬赏

            if self.config.stored.DailyGuildMission.is_expired():
                self.config.stored.DailyGuildMission.clear()

            # 签到
            self._sign_in()
            # 放河灯
            self._float_river_lantern()
            # 识别悬赏内容
            self.write_dungeon_plan()
            # 如果需要的话打沙盘
            if self.config.GuildActivity_ClearShaPanFlag:
                week = get_server_weekday()
                if week == 3 or week == 6:
                    logger.info("Today is Thursday or Sunday, run sha pan lun yi")
                    ShaPanLunYi(self.config,self.device).run()

            if self.config.Cosplay_SendCosplayStatus:
                Cosplay(self.config, self.device).run()

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
