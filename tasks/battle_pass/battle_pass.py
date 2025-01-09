from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.base.page import page_fuliwangchuan, page_main

from tasks.base.ui import UI
from tasks.battle_pass.assets.assets_battle_pass import *
from tasks.dispatch.channel import Channel
from tasks.dispatch.moments import Moments


class BattlePass(UI):
    """

    """

    def run(self):
        """
        """
        logger.hr('BattlePass', level=1)

        self.ui_ensure(page_fuliwangchuan)
        if self._goto_bp_page():
            self._goto_mission_page()
            self._get_reward_and_back()
            # 确定BP开了再做任务
            # 知交圈点赞三次
            if self.config.BattlePassStorage_MomentsGiveLike:
                Moments(self.config, self.device).run()
            # 世界频道发言两次 本来该在bp里写的但我懒得写bp
            if self.config.BattlePassStorage_ChannelSendIcon:
                Channel(self.config, self.device).run()

        self.ui_goto_main()
        self.config.task_call("DataUpdate")

        self.config.task_delay(server_update=True)

    def _goto_bp_page(self,skip_first_screenshot=True)->bool:
        """
        Returns:
            bool: if arrive chang-ping-wen-yin page successfully
        """
        timeout = Timer(10).start()
        # level = -1
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.warning('Get search battle pass page timeout')
                return False
            if self.appear(BP_PAGE_STABLE_CHECK):
                logger.info("BattlePass page arrived")
                return True
            if self.handle_reward():
                continue
            if self.handle_bp_level_up():
                continue
            if self.appear_then_click(GOTO_BP):
                timeout.reset()
                continue


    def _goto_mission_page(self, skip_first_screenshot=True):

        timeout = Timer(15).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.warning('Get open mission page timeout')
                break
            if self.appear(TODAY_MISSION_CHECK):
                logger.info("Open mission page, break")
                break
            if self.handle_reward():
                continue
            if self.handle_bp_level_up():
                continue
            if self.appear_then_click(LEVEL_REWARD_UNLOCK):
                continue

            if self.appear_then_click(MISSION_CLICK):
                continue


    def _get_reward_and_back(self,skip_first_screenshot=True):
        timeout = Timer(15).start()
        show = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.warning('Get back timeout')
                break

            # if self.appear(BP_PAGE_CHECK):
            #     logger.info("Return to battle pass main page, break")
            #     break
            if self.appear_then_click(LEVEL_REWARD_UNLOCK):
                continue
            if self.handle_reward():
                continue

            if self.appear(BP_PAGE_STABLE_CHECK):
                level = Digit(OCR_LEVEL).ocr_single_line(self.device.image)
                self.config.stored.BattlePassLevel.value = level
                logger.info(f"Battle pass page is stable, level:{level}")
                break

            if self.appear(BP_REWARD_LOCKED):
                self.appear_then_click(MISSION_CLOSE)
                if not show:
                    logger.info("No reward to get, go back")
                    show = True
                continue
            if self.appear_then_click(BP_REWARD_UNLOCK):
                continue


            if self.handle_bp_level_up():
                continue

if __name__ == '__main__':
    ui = BattlePass('fhlc')
    ui.device.screenshot()
    ui.run()
