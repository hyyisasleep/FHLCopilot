import traceback

from tasks.base.assets.assets_base_page import *
from tasks.office.assets.assets_office_visit import OTHER_OFFICE_CHECK


class Page:
    # Key: str, page name like "page_main"
    # Value: Page, page instance
    all_pages = {}

    @classmethod
    def clear_connection(cls):
        for page in cls.all_pages.values():
            page.parent = None

    @classmethod
    def init_connection(cls, destination):
        """
        Initialize an A* path finding among pages.

        Args:
            destination (Page):
        """
        cls.clear_connection()

        visited = [destination]
        visited = set(visited)
        while 1:
            new = visited.copy()
            for page in visited:
                for link in cls.iter_pages():
                    if link in visited:
                        continue
                    if page in link.links:
                        link.parent = page
                        new.add(link)
            if len(new) == len(visited):
                break
            visited = new

    @classmethod
    def iter_pages(cls):
        return cls.all_pages.values()

    @classmethod
    def iter_check_buttons(cls):
        for page in cls.all_pages.values():
            yield page.check_button

    def __init__(self, check_button):
        self.check_button = check_button
        self.links = {}
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self.name = text[:text.find('=')].strip()
        self.parent = None
        Page.all_pages[self.name] = self

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def link(self, button, destination):
        self.links[destination] = button


# Main page
page_main = Page(MAIN_GOTO_CHARACTER)

# 商铺
page_shop = Page(SHOP_CHECK)
page_shop.link(BACK,destination=page_main) # 妈耶喵居也能去
page_main.link(MAIN_GOTO_SHOP,destination=page_shop)


# 喵居
page_cattery = Page(CATTERY_CHECK)
page_cattery.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_CATTERY,destination=page_cattery)

# 名士谱
page_character = Page(CHARACTER_CHECK)
page_character.link(BACK, destination=page_main)
page_main.link(MAIN_GOTO_CHARACTER, destination=page_character)

# 每日必做
page_daily_quest = Page(DAILY_QUEST_CHECK)
page_daily_quest.link(BACK, destination=page_main)
page_main.link(MAIN_GOTO_DAILY_QUEST, destination=page_daily_quest)

# 福利忘川
page_fuliwangchuan = Page(FULI_AND_CHANGPING_CHECK)
page_fuliwangchuan.link(BACK, destination=page_main)
page_main.link(MAIN_GOTO_FULIWANGCHUAN, destination=page_fuliwangchuan)


# 互动
page_interact = Page(INTERACT_CHECK)
page_interact.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_INTERACT, destination=page_interact)

#==========================
# 秘境
page_mijing = Page(MIJING_CHECK)
page_mijing.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_MIJING, destination=page_mijing)
# 宝墟
page_baoxu = Page(BAOXU_CHECK)
page_baoxu.link(BACK,destination=page_mijing)
page_mijing.link(MIJING_GOTO_BAOXU,destination=page_baoxu)

# 宝墟编队
page_baoxu_prepare = Page(BAOXU_PREPARE_CHECK)
page_baoxu_prepare.link(BACK,destination=page_baoxu)
page_baoxu.link(BAOXU_JINGYUAN_GOTO_PREPARE,destination=page_baoxu_prepare)
# 镜渊
page_jingyuan = Page(JINGYUAN_CHECK)
page_jingyuan.link(BACK,destination=page_mijing)
page_mijing.link(MIJING_GOTO_JINGYUAN,destination=page_jingyuan)
# 镜渊编队
page_jingyuan_prepare = Page(JINGYUAN_PREPARE_CHECK)
page_jingyuan_prepare.link(BACK,destination=page_jingyuan)
page_jingyuan.link(BAOXU_JINGYUAN_GOTO_PREPARE,destination=page_jingyuan_prepare)

#故世风云
page_gushifengyun = Page(GUSHIFENGYUN_CHECK)
page_gushifengyun.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_GUSHIFENGYUN, destination=page_gushifengyun)


#===========================

# 金戈馆
page_jingeguan = Page(JINGEGUAN_CHECK)
page_jingeguan.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_JINGEGUAN, destination=page_jingeguan)

# 桃源居
page_office = Page(TAOYUAN_CHECK)
page_office.link(BACK, destination=page_main)
page_main.link(MAIN_GOTO_TAOYUAN, destination=page_office)

# 知交圈
page_moments = Page(MOMENTS_CHECK)
page_moments.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_MOMENTS, destination=page_moments)

#个人资料
page_profile = Page(PROFILE_CHECK)
page_profile.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_PROFILE, destination=page_profile)
# ====================================
# 雅社
page_guild = Page(GUILD_CHECK)
page_guild.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_GUILD, destination=page_guild)
# 雅社放河灯
page_guild_begging = Page(GUILD_BEGGING_CHECK)
page_guild_begging.link(BACK,destination=page_guild)
page_guild.link(GUILD_GOTO_BEGGING, destination=page_guild_begging)
# 雅社悬赏
page_guild_mission = Page(GUILD_MISSION_CHECK)
page_guild_mission.link(BACK,destination=page_guild)
page_guild.link(GUILD_GOTO_MISSION, destination=page_guild_mission)


# =============金戈馆================
page_jingeyanwu = Page(JINGEYANWU_CHECK)
page_jingeyanwu.link(BACK,destination=page_jingeguan)
page_jingeguan.link(JINGEGUAN_GOTO_JINGEYANWU,destination=page_jingeyanwu)

page_shapanlunyi = Page(SHAPANLUNYI_CHECK)
page_shapanlunyi.link(BACK,destination=page_jingeguan)
page_jingeguan.link(JINGEGUAN_GOTO_SHAPANLUNYI,destination=page_shapanlunyi)
# 金戈准备匹配界面，省的换完队还得退出去再开
page_jinge_prepare = Page(JINGEYANWU_PREPARE_CHECK)
page_jinge_prepare.link(BACK,destination=page_jingeyanwu)
page_jingeyanwu.link(JINGEYANWU_GOTO_PREPARE,destination=page_jinge_prepare)
# 七段以上的没奖励人机模式？加了下面这行之后就算点的是prepare也显示点no reward prepare- -
# page_jingeyanwu.link(JINGEYANWU_GOTO_NO_REWARD_PREPARE,destination=page_jinge_prepare)

# page_jingeyanwu.link(JINGEYANWU_GOTO_SHOP,destination=page_shop)
# page_shop.link(BACK,destination=page_jingeyanwu)
# =============桃源居================
# 桃源事务
page_office_affair = Page(TAOYUAN_AFFAIR_CHECK)
page_office_affair.link(BACK, destination=page_office)
page_office.link(TAOYUAN_GOTO_AFFAIR, destination=page_office_affair)
# 考工治图
page_office_jigsaw = Page(TAOYUAN_GAME_CHECK)
page_office_jigsaw.link(BACK, destination=page_office)
page_office.link(TAOYUAN_GOTO_GAME, destination=page_office_jigsaw)
# 用膳
page_office_meal = Page(TAOYUAN_MEAL_CHECK)
page_office_meal.link(BACK, destination=page_office)
page_office.link(TAOYUAN_GOTO_MEAL, destination=page_office_meal)
# 拜访他人
page_office_visit = Page(TAOYUAN_VISIT_CHECK)
page_office_visit.link(BACK, destination=page_office)
page_office.link(TAOYUAN_GOTO_VISIT, destination=page_office_visit)
# 他人的桃源居
page_other_office = Page(OTHER_OFFICE_CHECK)
page_other_office.link(BACK, destination=page_office_visit)

# 制造家具
page_office_furniture = Page(TAOYUAN_FURNITURE_CHECK)
page_office_furniture.link(BACK, destination=page_office)
page_office.link(TAOYUAN_GOTO_FURNITURE, destination=page_office_furniture)


