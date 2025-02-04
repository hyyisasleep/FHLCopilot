from module.base.utils import crop
from tasks.base.ui import UI

from module.base.timer import Timer
from module.logger import logger
from tasks.base.assets.assets_base_page import  BACK


from tasks.login.assets.assets_login import TIME_LIMIT_SIGN_IN_CHECK, TIME_LIMIT_SIGN_IN, TIME_LIMIT_SIGN_IN_EDGE, DAILY_SIGN_IN, DIVINE_CHECK
from tasks.login.assets.assets_login_activity_ticket_sign_in import *
from tasks.login.assets.assets_login_activity_guessing_celebrity import *

class SignInHandler(UI):

    def handle_guessing_celebrity_sign_in(self):
        """
        众里寻他活动道具签到：
            竖排签到单独一套UI
        Returns:
            bool: if page appear and handled
        """
        if self.appear(ZHONGLIXUNTA_PAGE_CHECK):
            logger.info("Zhong-li-xun-ta activity sign in page appear")
            return self._handle_activity_ticket_sign_in(ZHONGLIXUNTA_PAGE_CHECK,ZHONGLIXUNTA_SIGN_IN_CLICK,ZHONGLIXUNTA_SIGN_IN_CLICK_FINISH,ZHONGLIXUNTA_CLOSE)
        else:
            return False

    def handle_activity_ticket_sign_in(self):
        """
        活动门票签到：横着一排长达十几天那种，有个当期up名士看板
        """
        if self.appear(ACTIVITY_TICKET_SIGN_IN_PAGE_CHECK):
            logger.info("Activity ticket sign in page appear")
            return self._handle_activity_ticket_sign_in(ACTIVITY_TICKET_SIGN_IN_PAGE_CHECK,ACTIVITY_TICKET_SIGN_IN_CLICK,ACTIVITY_TICKET_SIGN_IN_CLICK_FINISH,ACTIVITY_TICKET_SIGN_IN_CLOSE)
        else:
            return False

    def _handle_activity_ticket_sign_in(self,
                                        page_check_button:ButtonWrapper,
                                        click_button:ButtonWrapper,
                                        click_finish_button:ButtonWrapper,
                                        close_button:ButtonWrapper)->bool:
        """
        发现页面出现时处理
        首先用一个循环检查需不需要签到（设置8s，签完了或者超时都算结束
        然后再用一个循环点关闭，但是这个没法查下一个界面是什么就还用超时判断结束
        Args:
            click_button :ButtonWrapper 点击签到的按钮
            click_finish_button :ButtonWrapper 检查今天签到已经完成的按钮，需要跟签到按钮在同一个地方（）
            close_button :ButtonWrapper 关闭当前页面
        Returns:
            bool: if sign in page appear and handled (now always true
        """
        click = False
        timeout = Timer(8).start()
        skip_first_screenshot = True
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

                if timeout.reached():
                    logger.info("Get timeout, close sign in page")
                    break
                if self.handle_reward():
                    continue
                if click and click_finish_button.match_template(
                        crop(self.device.image,click_finish_button.button), direct_match=True):
                    logger.info("Sign in finish, close sign in page")
                    break
                if self.appear_then_click(click_button):
                    click_finish_button.load_offset(click_button)
                    click = True
                    continue
        # 关闭界面
        skip_first_screenshot = True
        timeout = Timer(5).start()
        cnt = 0
        click = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.info("Get timeout, suggest sign in page is closed")
                break
            # 有时候会把签到页面一块点了 如果出现签到界面了就算关闭成功了……
            if self.appear(DAILY_SIGN_IN):
                logger.info("Daily sign in page appear, stop handling current activity sign in")
                break
            if click:
                if cnt > 3:
                    logger.info("Can't find sign in page,suggest sign in page is closed ")
                    break
                # not good but...
                if not self.appear(page_check_button,interval=1):
                    cnt += 1
                    continue
            if self.handle_reward():
                continue
            if self.appear_then_click(close_button, interval=2):
                click = True
                continue

        return True

    def handle_time_limit_sign_in(self):
        """
        福利忘川界面的限时送十连
        """
        if self.appear(TIME_LIMIT_SIGN_IN_CHECK):
            logger.info("Get time limit sign in page, try to get reward")
            timeout = Timer(10).start()
            skip_first_screenshot = True
            while 1:
                if skip_first_screenshot:
                    skip_first_screenshot = False
                else:
                    self.device.screenshot()
                    if timeout.reached():
                        logger.info("Get timeout, close sign in page")
                        self.appear_then_click(BACK)
                        break
                    if self.handle_reward():
                        logger.info("Get reward")
                        continue
                    # 这么写不对但是关了这界面下一个是啥。——。main？
                    if self.appear_then_click(TIME_LIMIT_SIGN_IN):
                        logger.info("Get time limit sign in gift")
                        continue
                    if self.appear_then_click(TIME_LIMIT_SIGN_IN_EDGE):
                        logger.info("Get time limit sign in gift(day 8, the label is on edge)")
                        continue


    def handle_daily_sign_in_reward(self):
        """
         每日签到
        """
        if self.appear_then_click(DAILY_SIGN_IN):
            logger.info("Sign in")
            return True
        if self.handle_reward():
            logger.info("Get sign in reward")
            # if self.handle_reward():
            #     logger.info("Get 5-day sign in reward")
            # 占卜吧
            return True

        if self.appear(DIVINE_CHECK):
            self.appear_then_click(BACK, interval=2)
            logger.info("Skip divine, sign in finish")
            return True

        return False


if __name__ == "__main__":
    ui = SignInHandler('fhlc')
    while 1:
        ui.device.screenshot()
        if ui.handle_activity_ticket_sign_in():
            break