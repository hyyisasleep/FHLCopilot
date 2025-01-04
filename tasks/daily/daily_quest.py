
from module.logger import logger


from tasks.cattery.cattery import Cattery
from tasks.daily.daily_quest_state import DailyQuestUI

from tasks.dispatch.dispatch import Dispatch

from tasks.office.office import Office

class DailyQuest(DailyQuestUI):

    def run(self):
        """

        """
        logger.hr('Daily Quest', level=1)

        Office(config=self.config, device=self.device).run()
        Cattery(config=self.config, device=self.device).run()
        Dispatch(config=self.config, device=self.device).run()
        # 更新一次活跃度
        if self.config.stored.DailyLiveness.is_expired():
            self.config.stored.DailyLiveness.clear()

        self.get_active_point_reward()

        self.config.task_delay(server_update=True)




if __name__ == '__main__':
    ui = DailyQuest('fhlc')
    ui.device.screenshot()
    ui.run()