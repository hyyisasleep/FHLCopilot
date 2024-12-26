
from module.logger import logger

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

    def run(self):
        """
        """
        logger.hr('Dungeon', level=1)
        # 打宝墟，不用打的话actual_times会置0
        actual_times = self.run_baoxu(self.config.stored.DailyBaoXuPlan.get_remain())
        if actual_times:
            self.config.stored.DailyBaoXuPlan.add(actual_times)
        # 打镜渊
        actual_times = self.run_jingyuan(self.config.stored.DailyJingYuanPlan.get_remain())
        if actual_times:
            self.config.stored.DailyJingYuanPlan.add(actual_times)
        # # TODO: 故世
        # actual_times = self.run_gushifengyun(self.config.stored.DailyGuShiFengYunPlan.get_remain())
        # if actual_times:
        #     self.config.stored.DailyGuShiFengYunPlan.add(actual_times)

