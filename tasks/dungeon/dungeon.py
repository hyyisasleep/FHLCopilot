import math

from module.config.utils import get_server_datetime
from module.logger import logger
from tasks.PVP.JinGeYanWu import JinGeYanWu
from tasks.base.page import page_main

from tasks.base.ui import UI
from tasks.combat.combat import Combat
from tasks.daily.daily_quest_state import DailyQuestUI


class Dungeon(Combat,DailyQuestUI):
    """
        根据雅社任务、每日活跃度缺失和体力补战斗
        活跃度上限：
        4次宝墟
        1次镜渊
        3次故世，但是故世还要写切换界面，不想写 摆了
        3次金戈
    """
    combat_power = 12

    def run(self):


        self.clear_daily_dungeon_plan()
        self.set_daily_dungeon_plan()
        self._run()

        self.get_active_point_reward()
        self.config.task_delay(server_update=True)

    def _run(self):
        """

        """
        logger.hr('Dungeon', level=1)


        if self.config.Dungeon_DailyJinGe:
            logger.info("Run Jin Ge plan")
            actual_times = (JinGeYanWu(config=self.config,device=self.device).
                            run_until_get_daily_reward(self.config.stored.DailyJinGePlan.get_remain()))
            if actual_times:
                self.config.stored.DailyJinGePlan.add(actual_times)

        # 打宝墟，不用打的话actual_times会置0
        cnt = 0
        while 1:
            if cnt > 3:
                logger.warning("Fail to finish bao xu plan after retrying 3 times, stop")
                break
            remain_times = self.config.stored.DailyBaoXuPlan.get_remain()
            if remain_times <= 0:
                break
            actual_times = self.run_baoxu(remain_times)
            self.config.stored.DailyBaoXuPlan.add(actual_times)
            cnt += 1

        # 打镜渊

        cnt = 0
        while 1:
            if cnt > 3:
                logger.warning("Fail to finish jing yuan plan after retrying 3 times, stop")
                break
            remain_times = self.config.stored.DailyJingYuanPlan.get_remain()
            if remain_times <= 0:
                break
            actual_times = self.run_jingyuan(remain_times)
            self.config.stored.DailyJingYuanPlan.add(actual_times)
            cnt += 1


        self.ui_ensure(page_main)



    def clear_daily_dungeon_plan(self):

        with self.config.multi_set():

            if self.config.stored.DailyBaoXuPlan.is_expired():
                self.config.stored.DailyBaoXuPlan.clear_total()
            if self.config.stored.DailyJingYuanPlan.is_expired():
                self.config.stored.DailyJingYuanPlan.clear_total()
            if self.config.stored.DailyGuShiFengYunPlan.is_expired():
                self.config.stored.DailyGuShiFengYunPlan.clear_total()
            if self.config.stored.DailyJinGePlan.is_expired():
                self.config.stored.DailyJinGePlan.clear_total()

    def jin_ge_has_priority(self):
        """
        判断今天是打宝墟还是打金戈，要是在金戈时间里就先打金戈，不然就先宝墟
        。。。以防有人一点半或者九点半开错过金戈时间，把判断时间提前了一个小时
        """
        use_jin_ge = self.config.Dungeon_DailyJinGe
        if use_jin_ge:
            _, _, level = JinGeYanWu(config=self.config, device=self.device).jin_ge_prepare()

            if level >= 6:
                now = get_server_datetime().hour
                if 11 <= now < 13 or 19 <= now < 21:
                    logger.info("Now jin ge is open(level > 6),")
                    return True
            else: # 六段以下随便打
                return True
        return False

    def set_daily_dungeon_plan(self):
        """
        根据当前活跃度算还要打什么
        我知道这样有坑，比如之前要是打过宝墟了还会傻呵呵的再刷4次宝墟。。。
        """
        logger.hr("Dungeon Plan",level=1)
        remains = math.ceil((100 - self.config.stored.DailyLiveness.value)/ 10)

        # 计算雅社任务打满够不够100，雅社只有故世镜渊宝墟
        bao_xu = max(self.config.stored.DailyBaoXuPlan.total,0)

        jing_yuan = max(self.config.stored.DailyJingYuanPlan.total,0)
        # gu_shi = min(self.config.stored.DailyGuShiFengYunPlan.total,3)

        jin_ge = 0

        remains -= (min(bao_xu,4) + min(jing_yuan,1))
        if remains <= 0:
            return True
        logger.info("Check jin ge priority")
        jin_ge_priority = self.jin_ge_has_priority()

        while remains > 0:
            remains -= 1
            if jin_ge_priority and jin_ge < 3:
                jin_ge += 1
            elif bao_xu < 4:
                bao_xu += 1
            elif jing_yuan < 1:
                jing_yuan += 1
            else:
                logger.warning("dungeon plan can't finish today's daily liveness, need manual help")



        logger.info(f"Today's plan: Bao Xu: {bao_xu} times, Jing Yuan: {jing_yuan} times, Jin Ge: {jin_ge} times")
        with self.config.multi_set():
            self.config.stored.DailyBaoXuPlan.set(value=0,total=bao_xu)
            self.config.stored.DailyJingYuanPlan.set(value=0,total=jing_yuan)
            # self.config.stored.DailyGuShiFengYunPlan.set(value=0,total=gu_shi)
            if self.config.Dungeon_DailyJinGe:
                self.config.stored.DailyJinGePlan.set(value=0,total=jin_ge)




if __name__ == '__main__':

    ui = Dungeon("fhlc")
    ui.device.screenshot()
    ui.run()