from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Digit

from tasks.base.page import page_office, page_office_furniture
from tasks.base.ui import UI

from tasks.office.affair import Affair

from tasks.office.jigsaw import Jigsaw
from tasks.office.meal import Meal

from tasks.office.assets.assets_office_furniture import *
from tasks.office.visit import Visit


class Office(UI):

    def run(self):
        """
        Run get support reward task
        """
        logger.hr('Taoyuan Office', level=1)
        # self.ui_ensure(page_cattery)
        # 主页去桃源居，有祝福就领\
        # self.ui_ensure(page_office)
        self.device.screenshot()
        self.ui_ensure(page_office)
        # 领午晚饭体力
        Meal(self.config, self.device).run()
        # 处理事务
        Affair(self.config, self.device).run()
        # 拜访拿花
        Visit(self.config, self.device).run()
        # 五天一回转化满的考工冶图道具
        if self.config.Office_TransKaoGongTicket:
            Jigsaw(self.config, self.device).run()
        # 打造随机家具 太简单了不放单独类写了。。。
        self._build_random_furniture()

        self.ui_goto_main()

        # self.config.task_delay(server_update=True)

    def _build_random_furniture(self):

        timeout = Timer(5).start()
        skip_first_screenshot = True
        self.ui_ensure(page_office_furniture)
        logger.info('Going to build random furniture')
        has_build = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if has_build:
                logger.info("Success build furniture")
                break

            if self.appear(BUILD_FURNITURE_FINISH):
                logger.info("No need build furniture")
                break

            if timeout.reached():
                logger.info("Get build furniture timeout")
                break

            # ocr看百工图数量
            bgt_ocr = Digit(OCR_BAIGONGTU_NUM, lang=self.config.LANG)
            num = bgt_ocr.ocr_single_line(self.device.image)

            if not has_build and num < 30:
                logger.info("baigongtu is not enough, cancel build furniture")
                break
            if self.appear_then_click(BUILD_FURNITURE_CHECK):
                continue
            # TODO:以后要是还有确定框就抽象成函数
            if self.appear_then_click(BUILD_FURNITURE_CONFIRM):
                has_build = True
                continue

        self.ui_ensure(page_office)


if __name__ == "__main__":
    ui = Office('fhlc')
    ui.device.screenshot()
    ui.run()
# path = r"C:\Users\huixi\Desktop\MuMu12-20240831-193937.png"
# ui.image_file = r"C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\午晚饭素材\MuMu12-20240831-193937.png"
# # import cv2
# # _ = LUNCH_FINISH.match_template(cv2.imread(os.fspath(path)),similarity=0.9)
# # print(LUNCH_FINISH.button_offset)
# print(ui.appear(LUNCH_FINISH,similarity=0.6))

# ui._convert_kaogong()
# ui.image_file = r'C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20240909-184813.png'
# print(ui.appear(BAIGONGTU_CONVERT_CLOSE))
# 测桃源居这仨字在不同背景下能不能被检测到，目前用了三张全检测到了
# 王阳明那个洞天没图，等遇到bug再说吧
# path = r'D:\myProject\FHLCopilot\testPicFolder'
# for file in os.listdir(path):
#     ui.image_file = os.path.join(path,file)
#     print(f"{file}:{ui.appear(TAOYUAN_CHECK)}")

# ui.image_file = r"C:\Users\huixi\Documents\MuMu共享文件夹\Screenshots\MuMu12-20240907-192155.png"
#
# print(ui.appear(GAME_BAIGONGTU_FULL_CHECK,similarity=0.6))
