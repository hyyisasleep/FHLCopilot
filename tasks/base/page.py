import traceback

from tasks.base.assets.assets_base_page import *


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
page_taoyuan = Page(TAOYUAN_CHECK)
page_taoyuan.link(BACK,destination=page_main)
page_main.link(MAIN_GOTO_TAOYUAN, destination=page_taoyuan)
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
page_taoyuan_affair = Page(TAOYUAN_AFFAIR_CHECK)
page_taoyuan_affair.link(BACK,destination=page_taoyuan)
page_taoyuan.link(TAOYUAN_GOTO_AFFAIR, destination=page_taoyuan_affair)
# 考工治图
page_taoyuan_game = Page(TAOYUAN_GAME_CHECK)
page_taoyuan_game.link(BACK,destination=page_taoyuan)
page_taoyuan.link(TAOYUAN_GOTO_GAME, destination=page_taoyuan_game)
# 用膳
page_taoyuan_meal = Page(TAOYUAN_MEAL_CHECK)
page_taoyuan_meal.link(BACK,destination=page_taoyuan)
page_taoyuan.link(TAOYUAN_GOTO_MEAL, destination=page_taoyuan_meal)
# 拜访他人
page_taoyuan_visit = Page(TAOYUAN_VISIT_CHECK)
page_taoyuan_visit.link(BACK,destination=page_taoyuan)
page_taoyuan.link(TAOYUAN_GOTO_VISIT, destination=page_taoyuan_visit)
# 制造家具
page_taoyuan_furniture = Page(TAOYUAN_FURNITURE_CHECK)
page_taoyuan_furniture.link(BACK,destination=page_taoyuan)
page_taoyuan.link(TAOYUAN_GOTO_FURNITURE, destination=page_taoyuan_furniture)


# # Team
# page_team = Page(TEAM_CHECK)
# page_team.link(CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_TEAM, destination=page_team)
#
# # Item, storage
# page_item = Page(ITEM_CHECK)
# page_item.link(CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_ITEM, destination=page_item)
#
# # Guide, which includes beginners' guide, daily missions and dungeons
# page_guide = Page(GUIDE_CHECK)
# page_guide.link(GUIDE_CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_GUIDE, destination=page_guide)
#
# # Gacha
# page_gacha = Page(GACHA_CHECK)
# page_gacha.link(CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_GACHA, destination=page_gacha)
#
# # Battle Pass
# page_battle_pass = Page(BATTLE_PASS_CHECK)
# page_battle_pass.link(CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_BATTLE_PASS, destination=page_battle_pass)
#
# # Event
# page_event = Page(EVENT_CHECK)
# page_event.link(CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_EVENT, destination=page_event)
#
# # Map
# page_map = Page(MAP_CHECK)
# page_map.link(CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_MAP, destination=page_map)
#
# # page_world, subpage of map, used to choose a world/planet e.g. Herta Space Station
# page_world = Page(WORLD_CHECK)
# page_world.link(BACK, destination=page_map)
# page_map.link(MAP_GOTO_WORLD, destination=page_world)
#
# # Tutorial
# page_tutorial = Page(TUTORIAL_CHECK)
# page_tutorial.link(CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_TUTORIAL, destination=page_tutorial)
#
# # Mission
# page_mission = Page(MISSION_CHECK)
# page_mission.link(CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_MISSION, destination=page_mission)
#
# # Message
# page_message = Page(MESSAGE_CLOSE)
# page_message.link(MESSAGE_CLOSE, destination=page_main)
# page_main.link(MAIN_GOTO_MESSAGE, destination=page_message)
#
# # Camera
# page_camera = Page(CAMERA_CHECK)
# page_camera.link(CLOSE, destination=page_menu)
# page_menu.link(MENU_GOTO_CAMERA, destination=page_camera)
#
# # Synthesize
# page_synthesize = Page(SYNTHESIZE_CHECK)
# page_synthesize.link(CLOSE, destination=page_menu)
# page_menu.link(MENU_GOTO_SYNTHESIZE, destination=page_synthesize)
#
# # Assignment
# page_assignment = Page(ASSIGNMENT_CHECK)
# page_assignment.link(CLOSE, destination=page_main)
# page_menu.link(MENU_GOTO_ASSIGNMENT, destination=page_assignment)
#
# # Forgotten Hall
# page_forgotten_hall = Page(FORGOTTEN_HALL_CHECK)
# page_forgotten_hall.link(CLOSE, destination=page_main)
#
# # Rogue, Simulated Universe
# page_rogue = Page(ROGUE_CHECK)
# page_rogue.link(CLOSE, destination=page_main)
#
# # Planner result
# page_planner = Page(PLANNER_CHECK)
# page_planner.link(CLOSE, destination=page_menu)
