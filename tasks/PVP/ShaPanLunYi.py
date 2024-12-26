
from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.PVP.assets.assets_pvp_sha_pan_lun_yi import *
from tasks.base.assets.assets_base_page import SHAPANLUNYI_CLOSE_CHECK, JINGEGUAN_GOTO_SHAPANLUNYI
from tasks.base.page import page_jingeguan, page_shapanlunyi
from tasks.base.ui import UI

class BuyFlagException(Exception):

    def __init__(self, str):
        super().__init__(str)

class ShaPanLunYi(UI):

    def run(self):

        logger.hr('Clear sha pan flag', level=1)
        # 新号在首页点金戈馆能点进履职书......算了都这进度了也别用自动化了
        # 沙盘没开或者用户没加雅社 先去金戈馆判断一下牌子是不是灰的
        #TODO: 周四周日23：10点以后看看牌子是不是灰的？

        self.ui_ensure(page_jingeguan)
        timeout = Timer(10).start()
        skip_first_screenshot = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.info("Get timeout when check sha pan is open or not, return")
                return
            if self.appear(SHAPANLUNYI_CLOSE_CHECK):
                logger.info("Sha pan lun yi isn't open, return")
                return
            if self.appear(JINGEGUAN_GOTO_SHAPANLUNYI):
                logger.info("Sha pan lun yi is open, continue")
                break
        self.ui_ensure(page_shapanlunyi)
        while 1:

            logger.hr("Start one sha pan combat", level=2)

            flag_ocr = Digit(FLAG_OCR, lang=self.config.LANG)
            flag_num = flag_ocr.ocr_single_line(self.device.image)

            try:
                self._run_sp()
            except BuyFlagException as e:
                logger.info(e)
                break

        # self.ui_goto_main()

    def _run_sp(self)->bool:
        if not self._refresh():
            return False
        if not self._attack():
            return False
        if not self._wait_until_get_reward():
            return False
        return True

    def _refresh(self, interval=2, skip_first_screenshot=True)->bool:
        click_refresh = False
        timeout = Timer(20).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning("Get refresh timeout")
                return False
            # 截的图会导致没拿到奖和拿到奖励的图被同时匹配上
            # 加个只有在UNLOCK和LOCKED状态才会出现的进度条做判定
            if self.appear(REWARD_CHECKED) and not self.appear(REWARD_PROGRESS_BAR):
                logger.info("No need refresh or refresh finish")
                return True
            if click_refresh and self.appear(REWARD_LOCKED):
                # 刷新时要等一会……
                continue
            if self.appear(REWARD_LOCKED) and self.appear_then_click(REFRESH,interval):
                logger.info("Use flag to refresh")
                continue
            if self.appear_then_click(REFRESH_CONFIRM):
                click_refresh = True
                continue
            # 避免上一回有奖励没领卡住的情况？
            if self.appear_then_click(REWARD_UNLOCK):
                logger.info("Get last round reward")
                continue
            if self.handle_reward():
                continue
            # 避免OCR抽风- -用尽了之后会提示买旗子，出现购买界面关掉就算打完
            if self.appear_then_click(FLAG_CLEAR_NOTICE) or self.appear_then_click(BUY_FLAG):
                raise BuyFlagException("Flag has been used up,don't buy flag and stop")

    def _attack(self, interval=2, skip_first_screenshot=True):
        timeout = Timer(10).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.info("Got start attack timeout")
                return False

            if self.appear(ATTACKING_CHECK,interval):
                logger.info("Attack start")
                return True
            if self.appear_then_click(ATTACK_START, interval):
                logger.info("E BA JIAN JUN prepare")
                continue
            if self.appear_then_click(ATTACK_CONFIRM, interval):
                logger.info("Start JIAN JUN combat")
                continue

    def _wait_until_get_reward(self, interval=2, skip_first_screenshot=True)->bool:
        timeout = Timer(10).start()
        # attack_finish = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.info("Got get reward timeout")
                return False

            # if attack_finish and self.appear_then_click(REWARD_UNLOCK):
            #     continue
            if self.handle_reward():
                # if attack_finish:
                #     logger.info("Get win time reward")
                # else:
                #     attack_finish = True
                #     logger.info("Get attack reward")
                continue
            if self.appear(REWARD_LOCKED) and self.appear(ATTACK_START):
                logger.info("Reward is locked,finish")
                return True
            # 有的时候会出现 进攻次数奖励弹窗冒出来前先把二胜奖励点了的鬼情况。。。
            # 但是用标记位好像也没用0.0
            if self.appear(ATTACK_START) and self.appear_then_click(REWARD_UNLOCK):
                logger.info("Attack finish and reward unlock")
                # attack_finish = True
                continue
            if self.appear(ATTACKING_CHECK,interval=5):
                logger.info("Attack continue")
                self.device.stuck_record_clear()
                timeout.reset()
                continue


if __name__ == '__main__':
    ui = ShaPanLunYi('fhlc')
    ui.device.screenshot()
    ui.run()

    # ui.image_file = r"C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20241103-130656.png"
    # print(ui.appear(SHAPANLUNYI_CLOSE_CHECK))
