

from module.logger import logger

from tasks.base.ui import UI
from tasks.cattery.cattery import Cattery
from tasks.combat.DailyCombat import DailyCombat
from tasks.daily.daily_quest_state import DailyQuestUI
from tasks.dispatch.dispatch import Dispatch
from tasks.office.office import Office


class DailyQuest(DailyQuestUI):

    def run(self):
        """

        """



        logger.hr('Daily Quest', level=1)

        self.claimed_point_reward = False

        Office(config=self.config, device=self.device).run()
        Cattery(config=self.config, device=self.device).run()
        Dispatch(config=self.config, device=self.device).run()
        # TODO: liveness check
        self.get_active_point_reward()
        # liveness = self._get_liveness_point()
        #
        DailyCombat(config=self.config, device=self.device).run()
        #
        # self._get_active_point_reward()
        if self.claimed_point_reward:
            self.config.task_call('DataUpdate')

        self.config.task_delay(server_update=True)


if __name__ == '__main__':
    ui = DailyQuest('fhlc')
    ui.device.screenshot()
    ui.run()