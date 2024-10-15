from module.logger import logger
from module.ui.switch import Switch
from tasks.base.page import page_shop
from tasks.base.ui import UI
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


# 这写法真的好丑啊（好丑啊
# 左侧菜单栏
TAB_STATE_PICK = 'Pick'
TAB_STATE_GIFT = 'Gift'
TAB_STATE_MONTHLY_CARD = 'MonthlyCard'
TAB_STATE_RESOURCE = 'Resource'
TAB_STATE_PVP = 'PVP'
TAB_STATE_PVE = 'PVE'
TAB_STATE_APPEARANCE = 'Appearance'
TAB_STATE_LEISURE = 'leisure'

# 子菜单
SUB_TAB_STATE_GIFT_DAILY = 'Gift_Daily'
SUB_TAB_STATE_LEISURE_CATTERY = 'Leisure_Cattery'
SUB_TAB_STATE_LEISURE_FRIENDSHIP = 'Leisure_Friendship'
SUB_TAB_STATE_RESOURCE_COPPER = 'Resource_Copper'

SWITCH_SHOP_TAB = ShopTabSwitch('ShopTab', is_selector=True)

# src KEYWORDS好像是用来做多语言适配的，但破游没这需求，开始阉割（）
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


class ShopUI(UI):
    # 把子菜单的搜索区域改成整个区域，懒得挨个截图改名了现加载吧
    # 有的时候日常那栏可能多个假日限定栏导致位置换掉了，其他的目前好像没动过，所以就不改搜索区域了
    GIFT_DAILY_CLICK.load_search(SUBTAB_SEARCH.area)
    GIFT_DAILY_CHECK.load_search(SUBTAB_SEARCH.area)

    def shop_tab_goto(self, state: str):
        """
            Args:
                state:
            Returns:
                bool: If UI switched
        """
        logger.hr('Shop tab goto', level=2)
        self.ui_ensure(page_shop)
        tab_switched = SWITCH_SHOP_TAB.set(state, main=self)
        # src后面的wait_loaded是检测过场动画的0.0 有用再说
        return tab_switched

    def shop_sub_tab_goto(self, state, skip_first_screenshot=True):
        """

        """
        logger.info(f"Goto {state} Page")
        if state == SUB_TAB_STATE_GIFT_DAILY:
            self.shop_tab_goto(TAB_STATE_GIFT)
            while 1:
                if skip_first_screenshot:
                    skip_first_screenshot = False
                else:
                    self.device.screenshot()
                if self.appear(GIFT_DAILY_CHECK):
                    return True
                if self.appear_then_click(GIFT_DAILY_CLICK):
                    continue
        elif state == SUB_TAB_STATE_LEISURE_CATTERY:
            self.shop_tab_goto(TAB_STATE_LEISURE)
            while 1:
                if skip_first_screenshot:
                    skip_first_screenshot = False
                else:
                    self.device.screenshot()
                if self.appear(LEISURE_CATTERY_CHECK):
                    return True
                if self.appear_then_click(LEISURE_CATTERY_CLICK):
                    continue
        elif state == SUB_TAB_STATE_LEISURE_FRIENDSHIP:
            self.shop_tab_goto("Leisure")
            while 1:
                if skip_first_screenshot:
                    skip_first_screenshot = False
                else:
                    self.device.screenshot()
                if self.appear(LEISURE_FRIENDSHIP_CHECK):
                    return True
                if self.appear_then_click(LEISURE_FRIENDSHIP_CLICK):
                    continue
        elif state == SUB_TAB_STATE_RESOURCE_COPPER:

            self.shop_tab_goto("Resource")
            while 1:
                if skip_first_screenshot:
                    skip_first_screenshot = False
                else:
                    self.device.screenshot()
                if self.appear(LEISURE_FRIENDSHIP_CHECK):
                    return True
                if self.appear_then_click(LEISURE_FRIENDSHIP_CLICK):
                    continue
        else:
            logger.warning(f"Can't goto {state}")
            return False

    def buy_goods(self, state, skip_first_screenshot=True):
        """
            Args:
                state:name of goods，example:?
                skip_first_screenshot:
            Returns:
                bool: If buy success
        """
        pass
