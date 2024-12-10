
import time


import os
import psutil
from pywinauto import Application, findwindows

# 检查微信进程是否已经运行
def is_wechat_running():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'WeChat.exe':
            return True
    return False

def handle_password_content(input:str)->str:
    res = input.split("：")
    return res[-1]
# 启动微信
def start_wechat():
    wechat_path = r"D:\WeChat\WeChat.exe"
    if not os.path.exists(wechat_path):
        raise FileNotFoundError(f"WeChat not found at {wechat_path}")
    app = Application('uia').start(wechat_path)

    # 查找并返回标题为“微信”的窗口
    dlg = app.window(title_re="微信")
    # 打印登录界面窗口结构
    # dlg.print_control_identifiers()

    # 查找并返回标题为“进入微信”的按钮并点击
    but = dlg.child_window(title="进入微信", control_type="Button")
    but.click_input()

    # 等待登录加载
    time.sleep(5)


    return app

def find_wechat_app():
    try:
        wechat_window = findwindows.find_window(title_re="微信")
        app = Application('uia').connect(handle=wechat_window)
        return app
    except Exception as e:
        return None
# 获取微信窗口
def find_wechat_window():
    try:
        wechat_window = findwindows.find_window(title_re="微信")
        app = Application('uia').connect(handle=wechat_window)
        return app.window(handle=wechat_window)
    except Exception as e:
        return None
#
def handle_sign_in():
    try:

        gzh = find_wechat_app().window(title_re="公众号")

        time.sleep(2)
        but = gzh.child_window(title_re="发消息")

        but.click_input()

    except Exception as e:
        print(e)
        return None

def handle_3():
    try:
        print("打开公众号消息界面")
        find_gzh = findwindows.find_window(title_re="忘川风华录手游")
        app = Application('uia').connect(handle=find_gzh)
        gzh = app.window(handle=find_gzh)

        but = gzh.child_window(title_re="福利上门")
        but.click_input()
        print("点击福利上门按钮")
        sign_in = gzh.child_window(title_re="每日签到",control_type="MenuItem")
        time.sleep(1)
        sign_in.click_input()
        print("打开每日签到界面")

        time.sleep(1)
        dialogList = gzh.child_window(title="消息",control_type="List")
        # 获取最后一条消息
        item = dialogList.children(control_type="ListItem")[-1]
        text = item.window_text()
        # 返回消息文本
        return handle_password_content(text)
    except Exception as e:
        print(e)

        return None
# 主逻辑
if __name__ == "__main__":
    if not is_wechat_running():
        print("微信未运行，正在启动...")
        start_wechat()

    print("查找微信窗口...")
    wechat_window = find_wechat_window()
    if wechat_window is None:
        print("未找到微信窗口，请检查是否启动成功或路径正确。")

    else:
        print("微信窗口已找到。")
        wechat_window.set_focus()

    # 切换到通讯录界面
        # wechat_window.print_control_identifiers(depth=3)
        navi = wechat_window.child_window(title_re="导航")
        if navi is None:
            print("找不到导航栏")
        else:
            # navi.print_control_identifiers(depth=3)
            # 切换到通讯录界面
            txl = navi.child_window(title_re="通讯录",control_type="Button")
            txl.click_input()
            print("切换到通讯录界面")


            gzh = wechat_window.child_window(title_re="公众号",control_type="ListItem")
            if gzh is None:
                print("找不到公众号")
            gzh = gzh.child_window(title_re="ContactListItem")
            gzh.click_input()
            print("切换到公众号界面")


            fhl = wechat_window.child_window(title_re="忘川风华录手游",control_type="ListItem")
            if fhl is None:
                print("没找到手游公众号")
            fhl.click_input()
            print("进入风华录公众号")

            time.sleep(2)
            # 进入公众号消息界面
            handle_sign_in()
            time.sleep(1)
            print(handle_3())
