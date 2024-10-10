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

    def shop(self):
        from tasks.shop.shop import DailyShop
        DailyShop(config=self.config, device=self.device).run()
    def taoyuanju(self):
        from tasks.taoyuanju.taoyuanju import Taoyuanju
        Taoyuanju(config=self.config, device=self.device).run()


if __name__ == '__main__':
    src = FHLCopilot('fhlc')
    src.loop()
