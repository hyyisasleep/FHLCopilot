
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
        3次金戈
    """
    combat_power = 12

    def run(self):
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
        #
        # actual_times = self.run_gushifengyun(self.config.stored.DailyGuShiFengYunPlan.get_remain())
        # if actual_times:
        #     self.config.stored.DailyGuShiFengYunPlan.add(actual_times)

    def test(self):
        cnt = 0
        while 1:
            if cnt > 3:
                logger.warning("Fail to finish bao xu plan after retrying 3 times, stop")
                break
            remain_times = 2
            if remain_times <= 0:
                break
            actual_times = self.run_baoxu(1)
            remain_times -= actual_times
            # self.config.stored.DailyBaoXuPlan.add(actual_times)
            cnt += 1


if __name__ == '__main__':

    ui = Dungeon("fhlc")
    ui.device.screenshot()
    ui.test()