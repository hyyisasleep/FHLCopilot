
from module.base.timer import Timer

from module.logger import logger
from module.ui.switch import Switch
from tasks.base.page import page_shop
from tasks.base.ui import UI
from tasks.shop.assets.assets_shop import BUY_GIFT_MAX_LOCK, BUY_GIFT_MAX_UNLOCK, GOODS_SOLD_CHECK, BUY_CONFIRM_FAIL, \
    REWARD_POPUP_CLOSED, SIGN_IN_PACK_SOLD_CHECK
from tasks.shop.assets.assets_shop_goods import *
from tasks.shop.assets.assets_shop_ui import *


class ShopTabSwitch(Switch):
    SEARCH_BUTTON = TAB_SEARCH

    def add_state(self, state, check_button, click_button=None):
        # Load search
        if check_button is not None:
            check_button.load_search(self.__class__.SEARCH_BUTTON.area)
        if click_button is not None:
            click_button.load_search(self.__class__.SEARCH_BUTTON.area)
        return super().add_state(state, check_button, click_button)

    def click(self, state, main):
        """
        Args:
            state (str):
            main (ModuleBase):
        """
        button = self.get_data(state)['click_button']
        _ = main.appear(button)  # Search button to load offset
        main.device.click(button)


# 这写法真的好丑啊
# 左侧菜单栏
TAB_STATE_PICK = 'Pick'
TAB_STATE_GIFT = 'Gift'
TAB_STATE_MONTHLY_CARD = 'MonthlyCard'
TAB_STATE_RESOURCE = 'RESOURCE'
TAB_STATE_PVP = 'PVP'
TAB_STATE_PVE = 'PVE'
TAB_STATE_APPEARANCE = 'Appearance'
TAB_STATE_LEISURE = 'LEISURE'

# 子菜单
SUB_TAB_STATE_GIFT_DAILY = 'GIFT_DAILY'
SUB_TAB_STATE_LEISURE_CATTERY = 'LEISURE_CATTERY'
SUB_TAB_STATE_LEISURE_FRIENDSHIP = 'LEISURE_FRIENDSHIP'
SUB_TAB_STATE_RESOURCE_COPPER = 'RESOURCE_COPPER'
SUB_TAB_STATE_PVP_JINGE = 'PVP_JINGE'
SWITCH_SHOP_TAB = ShopTabSwitch('ShopTab', is_selector=True)

# src KEYWORDS有多语言适配，但破游没这需求，开始阉割（）
SWITCH_SHOP_TAB.add_state(
    TAB_STATE_PICK,
    check_button=PICK_CHECK,
    click_button=PICK_CLICK
)
SWITCH_SHOP_TAB.add_state(
    TAB_STATE_GIFT,
    check_button=GIFT_CHECK,
    click_button=GIFT_CLICK
)
SWITCH_SHOP_TAB.add_state(
    TAB_STATE_MONTHLY_CARD,
    check_button=MONTHLY_CARD_CHECK,
    click_button=MONTHLY_CARD_CLICK
)
SWITCH_SHOP_TAB.add_state(
    TAB_STATE_RESOURCE,
    check_button=RESOURCE_CHECK,
    click_button=RESOURCE_CLICK
)
SWITCH_SHOP_TAB.add_state(
    TAB_STATE_PVP,
    check_button=PVP_CHECK,
    click_button=PVP_CLICK
)
SWITCH_SHOP_TAB.add_state(
    TAB_STATE_PVE,
    check_button=PVE_CHECK,
    click_button=PVE_CLICK
)
SWITCH_SHOP_TAB.add_state(
    TAB_STATE_APPEARANCE,
    check_button=APPEARANCE_CHECK,
    click_button=APPEARANCE_CLICK
)

SWITCH_SHOP_TAB.add_state(
    TAB_STATE_LEISURE,
    check_button=LEISURE_CHECK,
    click_button=LEISURE_CLICK
)


def analyze_goods_info(goods_button:ButtonWrapper)->list:
    """
    Args:
        goods_button :button's name
    Returns:
        [sub_tab_name,goods_name]
    """
    goods_name = goods_button.name

    splits = goods_name.split("_")
    # tab_name = splits[0]
    sub_tab_name = "_".join(splits[0:2])
    goods_name = "_".join(splits[3:])
    return [sub_tab_name,goods_name]


class ShopUI(UI):
    # 把子菜单的搜索区域改成整个区域，懒得挨个截图改名了现加载吧
    # 有的时候日常那栏可能多个假日限定栏导致位置换掉了，其他的目前好像没动过，所以就不改搜索区域了
    GIFT_DAILY_CLICK.load_search(SUBTAB_SEARCH.area)
    GIFT_DAILY_CHECK.load_search(SUBTAB_SEARCH.area)
    # 商店界面上下划中纵坐标是不改的，分四列搜索

    SHOWCASE_SEARCH_AREA = [[303, 125, 476, 690],[520, 125, 698, 690],
                            [744, 125, 918, 690],[963, 125, 1139, 690]]

    def buy_goods(self, goods_button, skip_first_screenshot=True) ->int:
        """
            Args:
                goods_button:goods icon，example:?
                skip_first_screenshot:
            Returns:
                bool: If buy success
        """
        sub_tab_name,goods_name = analyze_goods_info(goods_button)
        # 前往商店界面
        self.shop_sub_tab_goto(sub_tab_name,skip_first_screenshot)
        #find goods, some need drag down
        if self.search_goods(goods_button,skip_first_screenshot):
            if self.confirm_buy_goods(goods_button):
                return 1
        # TODO: 修改为返回购买数量
        else:
            # fail because many reasons?
            return 0


    def search_goods(self, goods_button:ButtonWrapper, skip_first_screenshot=True):
        """
        我是弱智之想了半天只想到一个分四列每一列搜一次，没搜到重新截个图重试两次，都没找到下滑一次 要是到底了就说找不到
        """
        retry_search_goods = 0
        drag_times = 0
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            self.device.screenshot()
            if self.goods_appear_in_cur_showcase(goods_button):
                return True
            else:
                retry_search_goods +=1
            # 我发现
            if drag_times > 5 or self.showcase_is_at_bottom() and retry_search_goods >= 3:
                logger.warning(f"Can't find {goods_button.name} in the whole showcase,break")
                return False
            # 可能出现打开栏把商品图标挡了的情况，但是加了也不会点，愁人
            # if self.handle_open_item_pack():
            #     retry_search_goods = 0
            #     continue
            if self.handle_reward():
                retry_search_goods = 0
                continue
            if retry_search_goods >= 3:
                logger.warning(f"Can't find {goods_button.name} at cur showcase after retrying 3 times,"
                               f"try to drag down")
                self.drag_button(SHOWCASE_DRAG_AREA,direction="up")
                drag_times += 1
                # 等待拉扯完成
                self.wait_until_showcase_is_stable()
                retry_search_goods = 0

    def wait_until_showcase_is_stable(self):
        """
        TODO:改了
        """
        timeout =Timer(2).start()
        while 1:
            if timeout.reached():
                break

    def showcase_is_at_bottom(self):
        if self.appear(SHOWCASE_BOTTOM_CHECK):
            return True
        if self.appear(SHOWCASE_NOT_BOTTOM_CHECK):
            return False
        return False

    def goods_appear_in_cur_showcase(self,goods_button:ButtonWrapper):
        for i in range(4):
            goods_button.load_search(self.SHOWCASE_SEARCH_AREA[i])
            if goods_button.match_template_luma(self.device.image,similarity=0.9):
                logger.info(f"{goods_button.name} appear at cur showcase's {i} column, break")
                return True
        return False




    def handle_choose_gift_num(self,interval):
        if self.appear_then_click(BUY_GIFT_MAX_LOCK,interval):
            logger.info("Buy max gift")
            return True
        if self.appear_then_click(BUY_GIFT_MAX_UNLOCK,interval):
            return True
        return False



    def confirm_buy_goods(self,goods_button:ButtonWrapper,skip_first_screenshot=True,interval=2):
        """
        确认买商品
        考虑资源不够的问题？
        """
        timeout = Timer(10).start()
        finish = False
        has_open_details = False
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if timeout.reached():
                logger.warning(f"Get buy {goods_button.name} timeout")
                break
            if self.appear(GOODS_SOLD_CHECK,interval):
                logger.info("goods is sold out, break")
                self.close_buy_details_popup()
                break
            if self.appear(SIGN_IN_PACK_SOLD_CHECK,interval):
                logger.info("Has got sign in pack, break")
                break
            if self.appear(BUY_CONFIRM_FAIL,interval):
                logger.info("Resource is not enough, choose not buy, break")
                self.close_buy_details_popup()
                break

            if finish and self.appear(REWARD_POPUP_CLOSED,interval):
                logger.info(f"Buy goods:{goods_button.name} finish")

                self.interval_reset(BUY_GIFT_MAX_UNLOCK)
                self.interval_reset(BUY_GIFT_MAX_LOCK)
                break
            if self.handle_reward(interval):
                timeout.reset()
                finish = True
                continue
            if self.handle_choose_gift_num(interval):
                timeout.reset()
                has_open_details = True
                continue
            if not has_open_details and self.appear_then_click(goods_button,interval):
                continue
        return True

    def shop_sub_tab_goto(self, state, skip_first_screenshot=True):
        """
            Args:
                state:name of sub tab
                skip_first_screenshot:
            Returns:
                bool: If switch sucess

            切换到二级菜单界面
        """
        logger.info(f"Goto {state} Page")
        if state == SUB_TAB_STATE_GIFT_DAILY:
            return self._shop_sub_tab_goto(TAB_STATE_GIFT, GIFT_DAILY_CHECK,
                                           GIFT_DAILY_CLICK, skip_first_screenshot)
        elif state == SUB_TAB_STATE_LEISURE_CATTERY:
            return self._shop_sub_tab_goto(TAB_STATE_LEISURE, LEISURE_CATTERY_CHECK,
                                           LEISURE_CATTERY_CLICK, skip_first_screenshot)

        elif state == SUB_TAB_STATE_LEISURE_FRIENDSHIP:
            return self._shop_sub_tab_goto(TAB_STATE_LEISURE, LEISURE_FRIENDSHIP_CHECK,
                                           LEISURE_FRIENDSHIP_CLICK, skip_first_screenshot)

        elif state == SUB_TAB_STATE_RESOURCE_COPPER:
            return self._shop_sub_tab_goto(TAB_STATE_RESOURCE, RESOURCE_COPPER_CHECK,
                                           RESOURCE_COPPER_CLICK, skip_first_screenshot)
        elif state == SUB_TAB_STATE_PVP_JINGE:
            return self._shop_sub_tab_goto(TAB_STATE_PVP, PVP_JINGE_CHECK,
                                           PVP_JINGE_CLICK, skip_first_screenshot)
        else:
            logger.warning(f"Can't goto {state}")
            return False

    def shop_tab_goto(self, state: str):
        """
            Args:
                state:name of tab
            Returns:
                bool: If UI switched
            切换到一级菜单界面
        """
        logger.hr('Shop tab goto', level=2)
        self.ui_ensure(page_shop)
        tab_switched = SWITCH_SHOP_TAB.set(state, main=self)
        # src后面的wait_loaded是检测过场动画的0.0 有用再说
        return tab_switched

    # 不是放着switchAPI不用是懒。。。有问题再改
    def _shop_sub_tab_goto(self, tab_check,sub_tab_check,sub_tab_click,skip_first_screenshot):
        """
        Args:
            tab_check:
            sub_tab_check:
            sub_tab_click:
            skip_first_screenshot:
        Returns:
            bool: If UI switched

        """
        self.shop_tab_goto(tab_check)
        timeout = Timer(10).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()
            if self.appear(sub_tab_check):
                return True
            if timeout.reached():
                logger.warning(f"Can't goto sub tab:{sub_tab_check.name}, stop to buy this tab's gift")
                return False
            if self.appear_then_click(sub_tab_click):
                continue
        return False

# 测图标能不能被找到用的
def match_check(ui):
    import os
    ROOT = './testPicFolder/Shop/'
    sub_dir = "cattery"
    folder_path = ROOT + sub_dir
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        ui.image_file = folder_path + '/'+ file_name
        print(file_name)
        print("TOY:"+str(ui.goods_appear_in_cur_showcase(LEISURE_CATTERY_GOODS_TOY)))
        print("FRAGMENT:" + str(ui.goods_appear_in_cur_showcase(LEISURE_CATTERY_GOODS_FRAGMENT)))
        print("BALL:"+str(ui.goods_appear_in_cur_showcase(LEISURE_CATTERY_GOODS_BALL)))
        print("GUBBIN:" + str(ui.goods_appear_in_cur_showcase(LEISURE_CATTERY_GOODS_GUBBINS)))

    sub_dir = "copper"
    folder_path = ROOT + sub_dir
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        ui.image_file = folder_path + '/' + file_name
        print(file_name)
        print("PUPPET:" + str(ui.goods_appear_in_cur_showcase(RESOURCE_COPPER_GOODS_COMMON_CAT_PUPPET)))
        print("CHAOS:" + str(ui.goods_appear_in_cur_showcase(RESOURCE_COPPER_GOODS_CHAOS_SPIRIT)))
        print("DYE:" + str(ui.goods_appear_in_cur_showcase(RESOURCE_COPPER_GOODS_DYE)))
        print("STONE:" + str(ui.goods_appear_in_cur_showcase(RESOURCE_COPPER_GOODS_LIGHTSTONE)))

    sub_dir = "friendship"
    folder_path = ROOT + sub_dir
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        ui.image_file = folder_path + '/' + file_name
        print(file_name)
        print("GIFT:" + str(ui.goods_appear_in_cur_showcase(LEISURE_FRIENDSHIP_GOODS_GIFT)))

    sub_dir = "sign_in_pack"
    folder_path = ROOT + sub_dir
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        ui.image_file = folder_path + '/' + file_name
        print(file_name)
        print("pack:" + str(ui.goods_appear_in_cur_showcase(GIFT_DAILY_GOODS_SIGN_IN_PACK)))

if __name__ == "__main__":
    ui = ShopUI("fhlc")

    print(ui.goods_appear_in_cur_showcase(SHOWCASE_BOTTOM_CHECK))



