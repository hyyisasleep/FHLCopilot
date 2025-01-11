import time

from module.base.timer import Timer
from module.config.utils import get_server_datetime
from module.logger import logger
from tasks.PVP.JinGeYanWu import JinGeYanWu
from tasks.PVP.assets.assets_pvp_zhu_lu import *
from tasks.combat.assets.assets_combat import WIN_CHECK


class ZhuLu(JinGeYanWu):

    @staticmethod
    def zhu_lu_wait()->bool:
        """
            正常逐鹿是19：x0开始准备，等到19：x1进战
            打完后回退到逐鹿星野界面，有个距本轮结束还有xx秒的设置
            19：5x打完之后，没了准备键Log就会疯狂刷PAGE_CHECK的log，应该得靠时间关闭
            不知道怎么写了先扔着吧
        """
        now = get_server_datetime()
        weekday = now.weekday()
        if weekday != 5:
            logger.warning("Today is not Saturday, stop")
            return False
        hour = now.hour

        if hour > 19:
            logger.warning("Zhu Lu is end after 20:00, stop")
            return False
        elif hour < 19:
            # TODO: wait until 19:00
            return True
        else:
            minute = now.minute
            minute_mod = minute % 10

            # 开启期间，十分钟

    def run(self,skip_first_screenshot=False):
        """
        现在这个等时间是，看到自动准备被勾上了就停20s（问题非常大，进ban位选择了还在等
        出来之后可能自动准备没勾，会看逐鹿星野页面等10s
        """
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.appear(AUTO_PREPARE_LOCKED):
                logger.info("Auto prepared finish,sleep 20 seconds")
                time.sleep(20)
                self.device.stuck_record_clear()
                continue
            if self.appear_then_click(AUTO_PREPARE_UNLOCK):
                continue
            if self.appear(ZHU_LU_PAGE_CHECK):
                logger.info("Wait for next zhu lu combat or open, sleep 10 seconds")
                time.sleep(10)
                self.device.stuck_record_clear()
                continue

            self._zhu_lu_combat()

    def _zhu_lu_combat(self,skip_first_screenshot=True,interval=5):
        """
            基本上跟金戈差不多，但是终止判定条件是跳到逐鹿界面
            还有胜负判定用的是普通胜利（所以用的combat asset里的），失败显示的是‘再接再厉’，但是我combat那里截的图不对所以又截了一个再字
            （好一个史山

            没处理预设队伍里有人被ban的情况。。。额。。。没见过啊。。。。
        """
        logger.hr("Run zhu-lu combat",level=2)

        while 1:

            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            timeout = Timer(20).start()

            if timeout.reached():
                logger.info("Get pvp timeout")
                break
            # 每局结束条件改为看到一局win或者fail之后再回到金戈演武界面，发现符为0之后没有获得奖励界面了
            #
            if self.appear(ZHU_LU_PAGE_CHECK):
                logger.info("One combat finish")
                break

            if self.handle_reward(interval):
                logger.info("Get pvp reward")
                finish_pvp = True
                continue

            if self.appear_then_click(WIN_CHECK, interval):
                logger.info("Get win")
                continue
            if self.appear_then_click(FAIL_CHECK, interval):
                logger.info("Get fail")
                continue
            if self.handle_rank_ten_mode_prepare(interval):
                timeout.reset()
                continue
            if self.handle_pvp_combat(interval):
                timeout.reset()
                continue

if __name__ == '__main__':
    ZhuLu('fhlc').run()