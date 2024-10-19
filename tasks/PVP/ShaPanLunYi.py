from pickle import FALSE

from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit
from tasks.PVP.assets.assets_pvp_ShaPanLunYi import *
from tasks.base.page import page_jingeguan, page_jingeyanwu
from tasks.base.ui import UI
# from tasks.office.assets.assets_office_affair import REWARD_UNLOCK

class BuyFlagException(Exception):

    def __init__(self, str):
        super().__init__(str)

class ShaPanLunYi(UI):

    def run(self):

        logger.hr('Clear sha pan flag', level=1)

        while 1:
            # self.device.screenshot()

            # logger.info("?")
            # self.device.screenshot()
            # self.ui_ensure(page_shapanlunyi)

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
        timeout = Timer(10).start()
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
        attack_finish = False
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
                if attack_finish:
                    logger.info("Get win time reward")
                else:
                    attack_finish = True
                    logger.info("Get attack reward")
                continue
            if self.appear(REWARD_LOCKED) and self.appear(ATTACK_START):
                logger.info("Reward is locked,finish")
                return True
            # 有的时候会出现 进攻次数奖励弹窗冒出来前先把二胜奖励点了的鬼情况。。。
            if (attack_finish and self.appear(ATTACK_START)
                    and self.appear_then_click(REWARD_UNLOCK)):
                logger.info("Attack finish and reward unlock")
                # attack_finish = True
                continue
            if self.appear(ATTACKING_CHECK,interval):
                logger.info("Attack continue")
                self.device.stuck_record_clear()
                timeout.reset()
                continue



    #TODO:加了该死的is_continue变量之后又开始一次刷俩旗了，不加还能运行
    # 0个旗的时候用查探领取会跳转到买旗界面，尼玛
    def _run_shapan(self, interval=5, skip_first_screenshot=False):
        finish = False
        has_start = False
        need_fresh = False
        is_continue = False
        while 1:

            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            timeout = Timer(20).start()

            if timeout.reached():
                logger.info("Get sha pan timeout")
                break
            if finish:
                break
            if self.appear_then_click(REFRESH_CONFIRM):
                logger.info("Refresh")
                finish = True
                continue

            if need_fresh and self.appear(REWARD_CHECK):
                need_fresh = False
                continue
            if self.appear_then_click(GET_REWARD_CONFIRM):
                # 第一次查探，确认获取六胜奖励
                continue

            if self.appear(COMBAT_CHECK, interval=1):
                logger.info("JIAN JUN continue")
                self.device.stuck_record_clear()
                timeout.reset()
                is_continue = True
                continue

            if need_fresh and self.appear_then_click(REFRESH):
                logger.info("Click refresh")
                continue
            if has_start and not is_continue and  self.appear_then_click(REFRESH):
                # self.handle_popup()
                logger.info("Click get reward")
                continue
            if not has_start and self.appear(REWARD_LOCK,interval,similarity=0.9):
                logger.info("Have got last round's reward,need refresh")
                need_fresh = True
                continue

            if is_continue and has_start and self.appear(COMBAT_PREPARE, interval):
                logger.info("Combat is end")
                is_continue =  False
                continue

            if not has_start and self.appear_then_click(COMBAT_PREPARE, interval):
                logger.info("E BA JIAN JUN prepare")
                continue
            if self.appear_then_click(COMBAT_START, interval):
                logger.info("Start JIAN JUN combat")
                has_start = True
                continue

            if self.handle_reward(interval):
                logger.info("Get pvp reward")

                continue




if __name__ == '__main__':
    ui = ShaPanLunYi('fhlc')
    ui.device.screenshot()
    ui.run()

    # ui.image_file = r"C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20241019-151413.png"
    # print(ui.appear(REWARD_CHECKED,similarity=0.95))
