
from module.base.timer import Timer
from module.exception import RequestHumanTakeover
from module.logger import logger
from module.ocr.ocr import DigitCounter

from tasks.base.page import page_jingyuan_prepare, page_baoxu_prepare, page_main
from tasks.base.ui import UI
from tasks.combat.assets.assets_combat import *


class CombatTimesOCR(DigitCounter):
    pass

class Combat(UI):
    """
        目前支持打宝墟和镜渊
        故世风云因为要切章每章还不一样懒得搞，而且一般刷完镜渊宝墟活跃度也满了，不写了
    """

    def run_baoxu(self,times)->int:
        """
        Returns:
            int:  success run times
        """
        if times == 0:
            return 0
        self.ui_ensure(page_baoxu_prepare)
        return self._run_combat(times)
        # self.ui_ensure(page_main)

    def run_jingyuan(self,times)->int:
        """
        Returns:
            int:  success run times
        """
        if times == 0:
            return 0
        self.ui_ensure(page_jingyuan_prepare)
        return self._run_combat(times)
        # self.ui_ensure(page_main)


    def _run_combat(self,times)->int:
        """
        Returns:
            int: run times
            中途中断是使用者的问题不是我的问题，溜了
        Pages:
            in: COMBAT_PREPARE
            out: COMBAT_PREPARE
        """
        if self._combat_prepare():
            # 设置次数
            actual_times = self._set_auto_combat_times(times)
            # 体力不够了或者其他什么bug，关弹窗
            if actual_times == 0:
                self.close_buy_details_popup()
                return 0
            # 开始挂机
            else:
                self._run_auto_combat()

                return actual_times

    def _close_set_auto_combat_popup(self, skip_first_screenshot=True):
        timeout = Timer(5).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get Close set auto combat popup timeout")
                break
            if self.appear_then_click(CLOSE_SET_AUTO_COMBAT, interval=2):
                continue
            # TODO:用背景颜色变化检测关没关

    def _select_team(self,team,skip_first_screenshot=True):

        timeout = Timer(10).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning(f"Get timeout, can't find team {team},use current team")
                break
            if team == 1:
                if self.appear(TEAM_ONE_CHECK):
                    logger.info("Switch to team 1")
                    return 1
                if self.appear_then_click(TEAM_ONE_CLICK):
                    continue
            elif team == 2:
                if self.appear(TEAM_TWO_CHECK):
                    logger.info("Switch to team 2")
                    return 2
                if self.appear_then_click(TEAM_TWO_CLICK):
                    continue
            elif team == 3:
                if self.appear(TEAM_THREE_CHECK):
                    logger.info("Switch to team 3")
                    return 3
                if self.appear_then_click(TEAM_THREE_CLICK):
                    continue
            elif team == 4:
                if self.appear(TEAM_FOUR_CHECK):
                    logger.info("Switch to team 4")
                    return 4
                if self.appear_then_click(TEAM_FOUR_CLICK):
                    continue
            elif team == 5:
                if self.appear(TEAM_FIVE_CHECK):
                    logger.info("Switch to team 5")
                    return 5
                if self.appear_then_click(TEAM_FIVE_CLICK):
                    continue
            else:
                logger.warning(f"Can't find team {team},use current team")
                break
        return 0


    def _combat_prepare(self, skip_first_screenshot=True):
        """
        在编队界面切换队伍+打开自动挂机弹窗设置
        """
        timeout = Timer(15).start()
        current_team = 0
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get combat prepare timeout")
                return False
            if self.appear(SET_AUTO_COMBAT_CHECK):
                break
            if self.appear(OPEN_SET_AUTO_COMBAT_FAILED):
                logger.warning("Can't start auto combat,because team is empty / not set cat assistant/ current level not cleared yet")
                raise RequestHumanTakeover
                # return False

            if current_team != self.config.Dungeon_Team:
                logger.info(f"Config need team {self.config.Dungeon_Team}")
                current_team = self._select_team(self.config.Dungeon_Team)
                continue
            # if self.appear_then_click(TEAM_FIVE_CLICK):
            #     logger.info("Switch to team 5")
            #     continue
            if self.appear_then_click(SKIP_BONUS):
                continue
            if self.appear_then_click(OPEN_SET_AUTO_COMBAT):
                continue
        return True

    def _run_auto_combat(self,skip_first_screenshot=True):
        """
        开始挂机→挂机结束
        """
        start_combat = False
        timeout = Timer(20).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get daily combat timeout")
                break
            if start_combat and self.appear(TEAM_FIVE_CHECK):
                logger.info("Auto combat end")
                break

            if self.appear_then_click(START_AUTO_COMBAT):
                continue
            if self.appear(COMBAT_CONTINUE_CHECK, interval=5):
                start_combat = True
                logger.info("Combat continue")
                timeout.reset()
                self.device.stuck_record_clear()
                continue
            if self.appear(AUTO_COMBAT_WAIT_BEFORE_START_CHECK,interval=5):
                logger.info("Wait countdown before start")
                timeout.reset()
                continue
            if self.appear_then_click(SKIP_MAO_CHE):
                logger.info("Check mao che, skip")
                timeout.reset()
                continue
            if self.appear_then_click(AUTO_COMBAT_END_CHECK):
                logger.info("Get auto combat reward")
                timeout.reset()
                continue


    def _set_auto_combat_times(self, times=1):


        combat_times_ocr = CombatTimesOCR(OCR_AUTO_TIMES, lang=self.config.LANG)
        cur_count, _, total_count = combat_times_ocr.ocr_single_line(self.device.image)
        # 体力攒多了可能会出现300/300点到地老天荒的情况，先拉一下
        if cur_count == total_count:
            self.drag_button(AUTO_TIMES_DRAG_AREA,direction="left")
            # 体力不够
        elif total_count == 1:
            return 0
        # TODO:计算各种不够的情况。。。。先假设体力是够的
        # 感恩src的伟大api
        self.ui_ensure_index(times,letter=combat_times_ocr,next_button=ADD_AUTO_TIMES_UNLOCK,
                             prev_button=SUB_AUTO_TIMES_UNLOCK,skip_first_screenshot=False)
        return times



if __name__ == '__main__':
    ui = Combat('fhlc')
    ui.run_jingyuan(1)