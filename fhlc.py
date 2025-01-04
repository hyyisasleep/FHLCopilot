from module.alas import AzurLaneAutoScript
from module.logger import logger
from tasks.battle_pass.battle_pass import BattlePass


class FHLCopilot(AzurLaneAutoScript):
    def restart(self):
        from tasks.login.login import Login
        Login(self.config, device=self.device).app_restart()

    def start(self):
        from tasks.login.login import Login
        Login(self.config, device=self.device).app_start()

    def stop(self):
        from tasks.login.login import Login
        Login(self.config, device=self.device).app_stop()

    def goto_main(self):
        from tasks.login.login import Login
        from tasks.base.ui import UI
        if self.device.app_is_running():
            logger.info('App is already running, goto main page')
            UI(self.config, device=self.device).ui_goto_main()
        else:
            logger.info('App is not running, start app and goto main page')
            Login(self.config, device=self.device).app_start()
            UI(self.config, device=self.device).ui_goto_main()

    def meal_power(self):
        from tasks.office.meal import Meal
        Meal(config=self.config, device=self.device).run()

    def shop(self):
        from tasks.shop.shop import DailyShop
        DailyShop(config=self.config, device=self.device).run()

    def guild(self):
        from tasks.guild.guild import Guild
        Guild(config=self.config, device=self.device).run()

    def daily_quest(self):
        from tasks.daily.daily_quest import DailyQuest
        DailyQuest(config=self.config, device=self.device).run()

    def battle_pass(self):
        from tasks.battle_pass.battle_pass import BattlePass
        BattlePass(config=self.config, device=self.device).run()

    def data_update(self):
        from tasks.item.data_update import DataUpdate
        DataUpdate(config=self.config, device=self.device).run()

    def daily_password(self):
        from tasks.daily.daily_password import DailyPassword
        DailyPassword(config=self.config, device=self.device).run()

    def clear_jin_ge_talisman(self):
        from tasks.PVP.JinGeYanWu import JinGeYanWu
        JinGeYanWu(config=self.config, device=self.device).run()

    def dungeon(self):
        from tasks.dungeon.dungeon import Dungeon
        Dungeon(config=self.config, device=self.device).run()


if __name__ == '__main__':
    src = FHLCopilot('fhlc')
    src.loop()


