from module.alas import AzurLaneAutoScript
from module.logger import logger


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

    def cattery(self):
        from tasks.cattery.cattery import Cattery
        Cattery(config=self.config, device=self.device).run()

    def daily_shop(self):
        from tasks.shop.shop import DailyShop
        DailyShop(config=self.config, device=self.device).run()

    def office(self):
        from tasks.office.office import Office
        Office(config=self.config, device=self.device).run()

    def dispatch(self):
        from tasks.dispatch.dispatch import Dispatch
        Dispatch(config=self.config, device=self.device).run()

    def guild(self):
        from tasks.guild.guild import Guild
        Guild(config=self.config, device=self.device).run()

if __name__ == '__main__':
    src = FHLCopilot('tqyb')
    src.loop()


