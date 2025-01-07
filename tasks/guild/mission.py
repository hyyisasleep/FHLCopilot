import re

from module.base.timer import Timer
from module.logger import logger
from module.ocr.ocr import Ocr
from tasks.base.page import page_guild_mission

from tasks.base.ui import UI
from tasks.guild.assets.assets_guild_mission import *


class GuildMissionOCR(Ocr):

    def after_process(self, result):
        result = re.sub(r'[，。："”“—]', '', result)
        # result = result.replace("赛社","雅社")
        if "蛙精"  in result or "蚌" in result:
            result = '击退4只蚌精'
        elif "心" in result:
            result = '击退5个镜之心魔'
        if '信物' in result:
            result = '完成1次雅社信物许愿'
        elif '故世' in result and '与' not in result:
            result = '故世风云困难战斗胜利2次'
        elif '消耗' in result:
            result = '消耗100贡献'
        else:
            # result = result.replace('贡肤', '贡献')
            # result = result.replace('贡站', '贡献')
            result = result.replace('登到','签到')
            result = result.replace('羁伴','羁绊')
            # result = result.replace('蚌格','蚌精')
        return super().after_process(result)
    pass


"""
2025-01-03 14:06:24.185 | INFO | [OCR_MISSION_1 after] 击退5个统之心魔 -> 击退5个镜之心魔                              
2025-01-03 14:06:24.187 | INFO | [OCR_MISSION_1 0.011s] 击退5个镜之心魔                                                
2025-01-03 14:06:24.196 | INFO | [OCR_MISSION_2 0.008s] 世风氧是提战斗胜                                               
2025-01-03 14:06:24.219 | INFO | [OCR_MISSION_2_MULTI_1 after] 故世风云困难战斗胜 -> 故世风云困难战斗胜利2次           
2025-01-03 14:06:24.220 | INFO | [OCR_MISSION_2_MULTI_1 0.021s] 故世风云困难战斗胜利2次                                
2025-01-03 14:06:24.242 | INFO | [OCR_MISSION_2_MULTI_2 0.020s] 利2次                                                  
2025-01-03 14:06:24.253 | INFO | [OCR_MISSION_3 0.009s] 每日必微透跃度达到                                             
2025-01-03 14:06:24.275 | INFO | [OCR_MISSION_3_MULTI_1 0.020s] 每日必做活跃度达到                                     
2025-01-03 14:06:24.299 | INFO | [OCR_MISSION_3_MULTI_2 0.020s] 100                                                    
2025-01-03 14:06:24.300 | INFO | Today's missions:['击退5个镜之心魔', '故世风云困难战斗胜利2次利2次',                  
'每日必做活跃度达到100']  

"""
# 剑荡风云：与xxx(任意一位至契名士)在故世风云困难战斗胜利3次
# 故世探秘：故世风云困难战斗胜利2次
# 镜渊破幻：击退5个镜之心魔
# 镜中镇幻：与xxx在镜渊战斗胜利3次
# 宝墟除恶：击退4只蚌精
# 宝墟求珍：与xxx在宝墟战斗胜利3次
# 结社共济：完成1次雅社签到
# 聊表寸心：提升1000点xxx与使君的羁绊值
# 大功告成：每日必做活跃度达到100
# 商铺交易：消耗100贡献
# 河灯许愿： 完成1次雅社信物许愿

class GuildMission(UI):

    button_list = [[OCR_MISSION_1,OCR_MISSION_1_MULTI_1,OCR_MISSION_1_MULTI_2],
                   [OCR_MISSION_2,OCR_MISSION_2_MULTI_1,OCR_MISSION_2_MULTI_2],
                    [OCR_MISSION_3,OCR_MISSION_3_MULTI_1,OCR_MISSION_3_MULTI_2]]
    # 拿关键词判断第一次识别的对不对，对了就不用当两行重新识别了
    ocr_dict = ["镜之心魔","镜渊","蚌精","宝墟","信物","消耗","签到","活跃度","羁绊值","故世","知交圈","合影","寻英","扮演"]

    def _scan_one_mission(self, buttons:list[ButtonWrapper]):
        """
        OCR识别雅社悬赏内容
        发现有的两行的委托一次识别不出来，只好换识别两行拼起来。。。。
        Args:
            buttons: 单行识别button，两行识别button的第一行和第二行
        Returns:
            str: 用is_result_matched 判断内容是否合理
        """

        def is_result_matched( result: str):
            return any(word in result for word in self.ocr_dict)


        single_ocr = GuildMissionOCR(buttons[0])
        single_result = single_ocr.ocr_single_line(self.device.image)
        if is_result_matched(single_result):
            return single_result
        else:
            multi_ocr_1 = GuildMissionOCR(buttons[1])
            multi_ocr_2 = GuildMissionOCR(buttons[2])
            multi_result = multi_ocr_1.ocr_single_line(self.device.image) + multi_ocr_2.ocr_single_line(self.device.image)
            if is_result_matched(multi_result):
                return multi_result
        return ""

    def _wait_until_mission_page_stable(self,skip_first_screenshot=True):
        """
        悬赏任务界面要加载一会，用右下角的小人判断是否稳定，省的OCR抽风
        """
        timeout = Timer(3, count=3).start()
        cnt = 0
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            # End
            if timeout.reached():
                logger.warning('Wait until mission page loaded timeout')
                return False
            if cnt > 3:
                logger.info('Mission page is loaded')
                return True
            if self.appear(MISSION_PAGE_STABLE_CHECK):

                cnt += 1
                continue

    def write_dungeon_plan(self):
        """
        OCR识别前三个悬赏
        写到config里
        如果有要打宝墟镜渊的就写到dungon plan里

        """

        # 清空
        with self.config.multi_set():
            if self.config.stored.DailyBaoXuPlan.is_expired():
                self.config.stored.DailyBaoXuPlan.clear_total()
            if self.config.stored.DailyJingYuanPlan.is_expired():
                self.config.stored.DailyJingYuanPlan.clear_total()
        # 跳转到悬赏界面
        self.ui_ensure(page_guild_mission)
        self._wait_until_mission_page_stable()
        # OCR
        contents = self.scan_daily_missions()
        # 算副本次数
        bao_xu = 0
        jing_yuan = 0
        # gu_shi_times = 0
        for content in contents:
            if "镜之心魔" in content:
                jing_yuan = max(jing_yuan, 2)
            elif "镜渊" in content:
                jing_yuan = max(jing_yuan, 3)
            elif "蚌精" in content:
                bao_xu = max(bao_xu, 2)
            elif "宝墟" in content:
                bao_xu = max(bao_xu, 3)
            # 故世没写

        logger.info(f"Today's dungeon plan: bao xu {bao_xu} times, jing_yuan {jing_yuan} times")

        # write to plan
        with self.config.multi_set():
            self.config.stored.DailyGuildMission.write_missions(contents)
            if bao_xu:
                self.config.stored.DailyBaoXuPlan.set(value=0, total=bao_xu)
            if jing_yuan:
                self.config.stored.DailyJingYuanPlan.set(value=0, total=jing_yuan)

    def scan_daily_missions(self):
        """
        OCR识别前三个悬赏
        方便测试
        """
        contents = [self._scan_one_mission(self.button_list[i]) for i in range(len(self.button_list))]
        logger.info(f"Today's missions:{contents}")
        return contents




if __name__ == '__main__':
    ui = GuildMission("fhlc")
    ui.image_file = None
    ui.device.screenshot()
    ui.write_dungeon_plan()

