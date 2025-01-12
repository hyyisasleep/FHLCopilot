
from module.base.timer import Timer
from module.logger import logger
from tasks.base.page import page_cattery
from tasks.base.ui import UI
from tasks.cattery.assets.assets_cattery import (
    NEED_FEED_CAT,
    FEED_CAT_REWARD,
    PLAY_WITH_CAT,
    SKIP_BUTTON, NO_NEED_FEED_CAT,PLAY_WITH_CAT_LOCKED,
)


class Cattery(UI):

    def run(self):

        logger.hr('Cattery', level=1)
        self.ui_ensure(page_cattery)

        finish_feed_cat = self._feed_cats()
        finish_play = self._play_with_cats()
        # TODO:躲猫猫 妈呀咋写啊
        # self._hide_and_seek()

        with self.config.multi_set():
            if finish_feed_cat:
                self.config.stored.CatteryFeedCat.set(finish_feed_cat)
            if finish_play:
                self.config.stored.CatteryPlayWithCat.set(finish_play)

        self.ui_goto_main()




    def _feed_cats(self, skip_first_screenshot=True)->int:
        finish = 0
        logger.hr('One-click feed cat', level=3)
        has_feed = False
        # empty = Timer(1, count=1).start()
        timeout = Timer(10).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.warning('Get feed cat timeout')
                break

            if self.handle_reward():
                logger.info('Get feed cat reward')
                continue

            if self.appear(NO_NEED_FEED_CAT):
                if has_feed:
                    logger.info('Feed cat finish')
                else:
                    logger.info('No need feed cat.')
                finish = 1
                break

            if self.appear_then_click(NEED_FEED_CAT, similarity=0.70):
                timeout.reset()
                continue

            if self.appear_then_click(FEED_CAT_REWARD, similarity=0.7):
                has_feed = True
                finish = 1
                timeout.reset()

                continue
        return finish

    def _play_with_cats(self, skip_first_screenshot=True)->int:
        logger.hr('One-click play with cat', level=3)
        finish = 0
        timeout = Timer(10).start()

        has_play = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if timeout.reached():
                logger.warning('Get [play with cat] timeout')
                break

            if self.handle_reward():
                logger.info('Get play with cat reward')
                continue

            if self.appear(PLAY_WITH_CAT_LOCKED):
                if has_play:
                    logger.info('Play with cat finish')
                else:
                    logger.info('No need play with cat')
                finish = 1
                break

            if self.appear_then_click(PLAY_WITH_CAT, similarity=0.70, interval=5):
                timeout.reset()
                has_play = True
                continue
            if self.appear_then_click(SKIP_BUTTON, similarity=0.70, interval=2):
                timeout.reset()
                finish = 1
                continue
        return finish
    def _hide_and_seek(self):
        pass



if __name__ == '__main__':
    ui = Cattery('fhlc')
    ui.device.screenshot()
    ui.run()
