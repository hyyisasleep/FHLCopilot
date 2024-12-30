

from module.logger import logger

from tasks.cattery.cattery import Cattery
from tasks.daily.daily_quest_state import DailyQuestUI
from tasks.dispatch.dispatch import Dispatch
from tasks.dungeon.dungeon import Dungeon
from tasks.office.office import Office

import math
class DailyQuest(DailyQuestUI):

    def run(self):
        """

        """
        logger.hr('Daily Quest', level=1)
        self.clear_daily_liveness_and_plan()

        self.claimed_point_reward = False

        Office(config=self.config, device=self.device).run()
        Cattery(config=self.config, device=self.device).run()
        Dispatch(config=self.config, device=self.device).run()

        self.get_active_point_reward()

        self.set_daily_dungeon_plan()
        Dungeon(config=self.config, device=self.device).run()

        self.get_active_point_reward()

        # if self.claimed_point_reward:
        #     self.config.task_call('DataUpdate')

        self.config.task_delay(server_update=True)

    def clear_daily_liveness_and_plan(self):

        with self.config.multi_set():
            if self.config.stored.DailyLiveness.is_expired():
                self.config.stored.DailyLiveness.clear_total()
            if self.config.stored.DailyBaoXuPlan.is_expired():
                self.config.stored.DailyBaoXuPlan.clear_total()
            if self.config.stored.DailyJingYuanPlan.is_expired():
                self.config.stored.DailyJingYuanPlan.clear_total()
            if self.config.stored.DailyGuShiFengYunPlan.is_expired():
                self.config.stored.DailyGuShiFengYunPlan.clear_total()
            if self.config.stored.DailyJinGePlan.is_expired():
                self.config.stored.DailyJinGePlan.clear_total()

    def set_daily_dungeon_plan(self):
        """
        根据当前活跃度算还要打什么
        我知道这样有坑，比如之前要是打过宝墟了还会傻呵呵的再刷4次宝墟。。。
        """
        remains = math.ceil((100 - self.config.stored.DailyLiveness.value)/ 10)

        # 计算雅社任务打满够不够100，雅社只有故世镜渊宝墟
        bao_xu = min(self.config.stored.DailyBaoXuPlan.total,4)
        jing_yuan = min(self.config.stored.DailyJingYuanPlan.total,1)
        # gu_shi = min(self.config.stored.DailyGuShiFengYunPlan.total,3)

        jin_ge = 0
        if (bao_xu + jing_yuan)>= remains:
            return True
        while remains > 0:
            if bao_xu < 4:
                bao_xu += 1
            elif jing_yuan < 1:
                jing_yuan += 1
            elif jin_ge < 3:
                jin_ge += 1
            # elif gu_shi < 3:
            #     gu_shi += 1

            remains -= 1
        # 没启用选项的话置0
        if not self.config.Dungeon_DailyJinGe:
            jin_ge = 0
        logger.info(f"Today's plan: Bao Xu: {bao_xu} times, Jing Yuan: {jing_yuan} times, Jin Ge: {jin_ge} times")
        with self.config.multi_set():
            self.config.stored.DailyBaoXuPlan.set(value=0,total=bao_xu)
            self.config.stored.DailyJingYuanPlan.set(value=0,total=jing_yuan)
            # self.config.stored.DailyGuShiFengYunPlan.set(value=0,total=gu_shi)
            if self.config.Dungeon_DailyJinGe:
                self.config.stored.DailyJinGePlan.set(value=0,total=jin_ge)




if __name__ == '__main__':
    ui = DailyQuest('fhlc')
    ui.device.screenshot()
    ui.run()