
from module.logger import logger
from tasks.PVP.JinGeYanWu import JinGeYanWu

from tasks.cattery.cattery import Cattery
from tasks.daily.daily_quest_state import DailyQuestUI
from tasks.daily.password.daily_password import DailyPassword

from tasks.dispatch.dispatch import Dispatch

from tasks.office.office import Office

class DailyQuest(DailyQuestUI):

    def run(self):
        """

        """
        logger.hr('Daily Quest', level=1)
        # 更新一次活跃度和任务完成列表
        if self.config.stored.DailyLiveness.is_expired():
            self.config.stored.DailyLiveness.clear()

            self.config.stored.CelebrityInteract.clear()
            self.config.stored.OfficeAffair.clear()
            self.config.stored.OfficeBuildFurniture.clear()
            self.config.stored.CatteryPlayWithCat.clear()
            self.config.stored.CatteryFeedCat.clear()
            self.config.stored.GetFriendshipPoint.clear()
            self.config.stored.AutoDailyPassword.clear()
            self.config.stored.JinGeDailyWinReward.clear()

        # 开始做日常
        Office(config=self.config, device=self.device).run()
        Cattery(config=self.config, device=self.device).run()
        Dispatch(config=self.config, device=self.device).run()

        if self.config.DailyQuestOptions_AutoDailyPassword:
            # 这个finish写配置写在run里面了
            DailyPassword(config=self.config,device=self.device).run()

        # 打金戈首胜奖励
        if self.config.DailyQuestOptions_DailyJinGeWinReward:
            win,_ = JinGeYanWu(config=self.config,device=self.device).run_until_get_daily_reward()
            if win:
                self.config.stored.JinGeDailyWinReward.set(1)


        self.get_active_point_reward()
        self.config.task_delay(server_update=True)




if __name__ == '__main__':
    ui = DailyQuest('fhlc')
    ui.device.screenshot()
    ui.run()