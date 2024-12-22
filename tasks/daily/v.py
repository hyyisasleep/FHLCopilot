

import time



from module.logger import logger
import os
import psutil
from pywinauto import Application, findwindows, WindowSpecification,timings,Desktop
import win32api
import win32con


class State:
    def __init__(self ,parent_window :WindowSpecification ,title_re :str ,control_type=""):
        self.parent_window = parent_window
        self.title_re = title_re
        self.control_type= control_type


    def target(self)->WindowSpecification:
        if self.control_type == "":
            target = self.parent_window.child_window(title_re= self.title_re)
        else:
            target = self.parent_window.child_window(title_re=self.title_re ,control_type=self.control_type)
        return target

    def appear(self):
        try:
            child = self.target()
            if not child.exists():
                # child.wait('visible')
                return False
            else:
                child.draw_outline()
                return True
        # TODO: what exception
        except Exception as e:
            print(e)
            return False
        pass

def appear_then_click(cur_state :State ,next_state :State):
    """
    for i in range(3):
        self.target().click_input():
        if next_state.target() appear:
            break
        else:
            time.sleep(5)

    """
    for i in range(5):
        if cur_state.appear():
            cur_state.target().click_input()

        if next_state.appear():
            print("appear")
            return True
        else:
            print("not appear，sleep 5s")
            time.sleep(5)
    print(f"Timeout when click {cur_state.title_re}")


def find_wechat_app():
    try:
        wechat_window = findwindows.find_window(title_re="微信")
        app = Application('uia').connect(handle=wechat_window)
        return app
    except Exception as e:
        print(e)
        return None

def get_psw_script():

    # skip launch wechat

# 定位左侧边栏导航
        wechat_window = find_wechat_app().window(title_re="微信")
        wechat_window.set_focus()
        navi = State(wechat_window,title_re="导航")
        #navi.appear()
        txl_window = State(navi.target(),title_re="通讯录",control_type="Button")


        gzh = State(wechat_window,title_re="公众号",control_type="ListItem")


        appear_then_click(txl_window, gzh)
        # navi = search_window(wechat_window,title_re="导航")
        # # 点击通讯录键 切换到通讯录界面
        # click_window(navi,title_re="通讯录",control_type="Button")
        # # 找联系人中公众号，应该不用划
        # gzh = search_window(wechat_window,title_re="公众号",control_type="ListItem")
        # # 按公众号键的真正按键ContactListItem
        # click_window(gzh,title_re="ContactListItem")
        # # 右边出现很多关注的公众号图标，点击焚化炉头像
        # # ……应该不用划吧
        # click_window(wechat_window,title_re="忘川风华录手游",control_type="ListItem")
        # # 会开一个新的窗口，焚化炉公众号详情界面

if __name__ == '__main__':
    get_psw_script()