import re

from module.base.timer import Timer
from module.base.utils import crop
from module.logger import logger
from module.ocr.ocr import Digit, DigitCounter
from tasks.base.page import page_main
from tasks.base.ui import UI
from tasks.item.assets.assets_item import *


class CopperOCR(Digit):

    def after_process(self, result):
        ":1391万"
        result = super().after_process(result)
        result = re.sub(r'[:.,。]', '', result)
        return result



class TongBaoOCR(Digit):
    pass

class PowerOCR(DigitCounter):

    def after_process(self, result):
        # from SRC
        # result = super().after_process(result)

        result = result.replace(r'1\.|[.]+', '/')

        result = re.sub(r'1150', '/150', result)

        result = re.sub(r'15$', '150', result)

        result = result.replace('/1501', '/150')
        result = result.replace('1.150$', '/150')
        # 12801:250  -> 1280/250
        result = result.replace('1:150$', '/150')
        #020191:150
        # 15541250 -> 1554/250
        result = re.sub(r'1250$', '/250', result)

        result = re.sub(r'25$', '250', result)

        result = result.replace('/2501', '/250')
        # 15541.250 -> 1554/250
        result = result.replace('1.250$', '/250')
        # 12801:250  -> 1280/250
        result = result.replace('1:250$', '/250')
        return super().after_process(result)

class DataUpdate(UI):


    def run(self):

        self.ui_ensure(page_main)
        tong_bao,power,total = self.get_tong_bao_and_power_status(self.device.image)
        copper = self.get_copper_status()
        logger.info(f"Copper:{copper}  TongBao:{tong_bao} Power:{power}/{total} ")

        self.write_config(copper,tong_bao,power,total)
        self.config.task_delay(server_update=True)


    def write_config(self,copper,tong_bao,power,total):
        with self.config.multi_set():
            if copper:
                self.config.stored.Copper.value = copper
            if tong_bao:
                self.config.stored.TongBao.value = tong_bao
            if power:
                # if self.config.stored.MonthlyCard30.value > 0 or self.config.stored.MonthlyCard68 > 0:
                #     # 有月卡的时候上限250，但是应该OCR自己就能认
                self.config.stored.Power.set(power,total=total)
                # else:
                #     self.config.stored.Power.set(power,total=150)

    def get_copper_status(self,skip_first_screenshot=True):
        COPPER_ICON.load_search(ICON_SEARCH.area)
        copper = None
        # if COPPER_ICON.match_template(self.device.image):
        #     COPPER_OCR.load_offset(COPPER_ICON)
        timeout = Timer(10).start()
        while 1:
            if skip_first_screenshot :
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if copper is not None:
                break
            if timeout.reached():
                logger.warning("Get copper ocr timeout")
                break

            if self.appear(COPPER_DETAIL_ICON):
                # logger.info(f"Offset:{COPPER_DETAIL_ICON.button_offset}")
                COPPER_DETAIL_OCR.load_offset(COPPER_DETAIL_ICON)
                COPPER_DETAIL_BACKGROUND.load_offset(COPPER_DETAIL_ICON)
                # .button直接把offset和area一起取了
                im = crop(self.device.image,COPPER_DETAIL_OCR.button,copy=False)
                copper = CopperOCR(COPPER_DETAIL_OCR).ocr_single_line(im,direct_ocr=True)
                continue

            if self.appear_then_click(COPPER_ICON):
                continue
        if self.appear(COPPER_DETAIL_ICON):
            self.close_popup(COPPER_ICON,COPPER_DETAIL_BACKGROUND)
        return copper

    @staticmethod
    def get_tong_bao_and_power_status(image):
        """
        Update copper, tong bao, power

        Returns:
            int|None: copper
            int|None: tong bao
            int|None: power
        """
        for button in [ TONGBAO_ICON, POWER_ICON]:
            button.load_search(ICON_SEARCH.area)

        # copper = self.get_copper_status(image)
        # copper = None
        # if COPPER_ICON.match_template(image):
        #     COPPER_OCR.load_offset(COPPER_ICON)
        #     im = crop(image, COPPER_OCR.button, copy=False)
        #     copper = CopperOCR(COPPER_OCR).ocr_single_line(im, direct_ocr=True)


        tong_bao = None
        if TONGBAO_ICON.match_template(image):
            TONGBAO_OCR.load_offset(TONGBAO_ICON)
            im = crop(image, TONGBAO_OCR.button, copy=False)
            tong_bao = TongBaoOCR(TONGBAO_OCR).ocr_single_line(im, direct_ocr=True)
            # if reserved > 2400:
            #     logger.warning(f'Unexpected reserved value: {reserved}')
            #     reserved = None

        power = None
        total=150
        if POWER_ICON.match_template(image):
            POWER_OCR.load_offset(POWER_ICON)
            im = crop(image, POWER_OCR.button, copy=False)
            power, _, total = PowerOCR(POWER_OCR).ocr_single_line(im, direct_ocr=True)
            if total != 150 and total != 250:
                logger.warning(f'Unexpected power total: {total}')
                power = None
                total = None


        return [tong_bao, power,total]


if __name__ == '__main__':
    ui = DataUpdate('fhlc')
    ui.device.screenshot()
    ui.get_copper_status()