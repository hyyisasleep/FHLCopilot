
from module.logger import logger
from tasks.PVP.JinGeYanWu import JinGeYanWu
from tasks.base.page import page_main

from tasks.base.ui import UI
from tasks.combat.combat import Combat


class Dungeon(Combat):
    """
        根据雅社任务、每日活跃度缺失和体力补战斗
        活跃度上限：
        4次宝墟
        1次镜渊
        3次故世，但是故世还要写切换界面，不想写 摆了
    """
    combat_power = 12

    def run(self):
        """
        加了个根据体力算打本的判断，人家src是能智能后置的但我懒得改了，这游戏还有体力清空的时候吗。。。
        """
        logger.hr('Dungeon', level=1)
        # 打宝墟，不用打的话actual_times会置0
        actual_times = self.run_baoxu(self.config.stored.DailyBaoXuPlan.get_remain())

        power = self.config.stored.Power.value
        if power >= actual_times * self.combat_power:
            cnt = 0
            while actual_times:
                self.config.stored.DailyBaoXuPlan.add(actual_times)
                if cnt > 3:
                    logger.warning("Try to achieve bao xu plan after retrying 3 times, stop")
                    break
                actual_times = self.run_baoxu(self.config.stored.DailyBaoXuPlan.get_remain())
                cnt += 1
            power -= actual_times * self.combat_power

        # 打镜渊
        cnt = 0
        actual_times = self.run_jingyuan(self.config.stored.DailyJingYuanPlan.get_remain())

        if power >= actual_times * self.combat_power:
            while actual_times:

                if cnt > 3:
                    logger.warning("Try to achieve jing yuan plan after retrying 3 times, stop")
                    break
                self.config.stored.DailyJingYuanPlan.add(actual_times)
                actual_times = self.run_jingyuan(self.config.stored.DailyJingYuanPlan.get_remain())
                cnt += 1

        if self.config.Dungeon_DailyJinGe:
            actual_times = JinGeYanWu.run_until_get_daily_reward(self.config.stored.DailyJinGePlan.get_remain())
            if actual_times:
                self.config.stored.DailyJinGePlan.add(actual_times)


        self.ui_ensure(page_main)
        #
        # actual_times = self.run_gushifengyun(self.config.stored.DailyGuShiFengYunPlan.get_remain())
        # if actual_times:
        #     self.config.stored.DailyGuShiFengYunPlan.add(actual_times)

