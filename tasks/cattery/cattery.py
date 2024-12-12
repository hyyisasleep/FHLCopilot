from module.base.timer import Timer
from module.logger import logger
# from tasks.base.assets.assets_base_page import CATTERY_CHECK, MAIN_GOTO_CATTERY
from tasks.base.page import page_cattery
from tasks.base.ui import UI
from tasks.cattery.assets.assets_cattery import (
    NEED_FEED_CAT,
    FEED_CAT_REWARD,
    PLAY_WITH_CAT,
    SKIP_BUTTON, NO_NEED_FEED_CAT,
)


class Cattery(UI):

    def run(self):
        """
        Run get support reward task
        """
        logger.hr('Cattery\'s affair', level=1)
        self.ui_ensure(page_cattery)

        self._feed_cats()
        self._play_with_cats()
        # TODO:躲猫猫 妈呀咋写啊
        self._hide_and_seek()
        self.ui_goto_main()

        self.config.task_delay(server_update=True)


    def _feed_cats(self, skip_first_screenshot=True):
        """
                Pages:
                    in: PROFILE
                    out: reward_appear()
                """
        logger.hr('One-click feed cat', level=3)
        has_feed = False
        # empty = Timer(1, count=1).start()
        timeout = Timer(10).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            # TODO: 用OCR判断幸福度不到100的情况下还没有一键喂猫，说明没到自动水平

            if has_feed:
                logger.info('Feed cat finish')
                break
            # if self.reward_appear():
            #
            #     break
            # if self.handle_reward():
            #     logger.info('Got feed cat reward')
            #     break
            # if self.appear(REWARD_POPUP):
            #     logger.info('Got reward popup')
            #     break
            if timeout.reached():
                logger.warning('Get feed cat timeout')
                break
            if self.appear(NO_NEED_FEED_CAT):
                logger.info('No need feed cat.')
                break
            if self.handle_reward():
                logger.info('Get feed cat reward')
                has_feed = True
                # timeout.reset()
                continue
            # if hasFeed and self.handle_reward():
            #     logger.info('Got [play with cat] reward')
            #     break

            if self.appear_then_click(NEED_FEED_CAT, similarity=0.70, interval=5):
                timeout.reset()
                continue

            if self.appear_then_click(FEED_CAT_REWARD, similarity=0.7, interval=5):
                timeout.reset()
                continue

        pass

    def _play_with_cats(self, skip_first_screenshot=True):
        logger.hr('One-click play with cat', level=3)

        empty = Timer(1, count=1).start()
        timeout = Timer(10).start()
        # 判断是不是在动画里，
        in_flash = False
        # 领完奖再走，遵循wiki的不要把click写在break上
        got_reward = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if not in_flash and empty.reached():
                logger.info('No need play with cat')
                break
            if got_reward:
                logger.info('Play with cat finished')
                break
            if timeout.reached():
                logger.warning('Get [play with cat] timeout')
                break
            if self.handle_reward():
                logger.info('Get play with cat reward')
                got_reward = True
                continue
            if self.appear_then_click(PLAY_WITH_CAT, similarity=0.70, interval=5):
                in_flash = True
                timeout.reset()
                continue
            if self.appear_then_click(SKIP_BUTTON, similarity=0.70, interval=2):
                timeout.reset()
                continue

    def _hide_and_seek(self):
        pass


# if __name__ == '__main__':
#     self = Cattery('fhlc')
#     self.device.screenshot()
#     self.run()
