

from module.logger import logger

from tasks.base.ui import UI
from tasks.cattery.cattery import Cattery
from tasks.combat.DailyCombat import DailyCombat
from tasks.dispatch.dispatch import Dispatch
from tasks.office.office import Office


class DailyQuest(UI):

    def run(self):
        """

        """
        logger.hr('Daily Quest', level=1)
        Office(config=self.config, device=self.device).run()
        Cattery(config=self.config, device=self.device).run()
        Dispatch(config=self.config, device=self.device).run()
        # TODO: liveness check

        DailyCombat(config=self.config, device=self.device).run()

