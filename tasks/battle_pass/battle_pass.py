
from module.logger import logger

from tasks.base.ui import UI


class BattlePass(UI):
    """
        根据雅社任务、每日活跃度缺失和体力补战斗
        活跃度上限：
        4次宝墟
        1次镜渊
        3次故世
    """

    def run(self):
        """
        """
        logger.hr('BattlePass', level=1)
        # self.run_baoxu(times=4)
        self.config.task_call("DataUpdate")

        self.config.task_delay(server_update=True)