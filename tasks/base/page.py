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
page_main.link(MAIN_GOTO_CHARACTER, destination=page_daily_quest)

# 福利忘川
page_fuliwangchuan = Page(FULI_AND_CHANGPING_CHECK)
page_fuliwangchuan.link(BACK, destination=page_main)
page_main.link(MAIN_GOTO_FULIWANGCHUAN, destination=page_fuliwangchuan)

# 故世风云，见鬼了这个也能从秘境进
page_gushi = Page(GUSHIFENGYUN_CHECK)
page_gushi.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_GUSHIFENGYUN, destination=page_gushi)
# 互动
page_interact = Page(INTERACT_CHECK)
page_interact.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_INTERACT, destination=page_interact)
# 秘境
page_mijing = Page(MIJING_CHECK)
page_mijing.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_MIJING, destination=page_mijing)
# 金戈馆
page_jingeguan = Page(JINGEGUAN_CHECK)
page_jingeguan.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_JINGEGUAN, destination=page_jingeguan)
#商铺
page_gushifengyun = Page(GUSHIFENGYUN_CHECK)
page_gushifengyun.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_GUSHIFENGYUN, destination=page_gushifengyun)
# 桃源居
page_office = Page(TAOYUAN_CHECK)
page_office.link(BACK, destination=page_main)
page_main.link(MAIN_GOTO_TAOYUAN, destination=page_office)
# 雅社
page_yashe = Page(YASHE_CHECK)
page_yashe.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_YASHE, destination=page_yashe)

# =============金戈馆================
page_jingeyanwu = Page(JINGEYANWU_CHECK)
page_jingeyanwu.link(BACK,destination=page_jingeguan)
page_jingeguan.link(JINGEGUAN_GOTO_JINGEYANWU,destination=page_jingeyanwu)
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


