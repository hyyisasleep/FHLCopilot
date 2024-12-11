
import time
from module.logger import logger
import os
import psutil
from pywinauto import Application, findwindows, WindowSpecification
import win32api
import win32con


def click_window(parent_window:WindowSpecification,title_re:str,control_type="",interval=2):
    dst = search_window(parent_window,title_re,control_type,interval)
    if dst is None:
        raise Exception("Could not find the window")

    else:
        dst.click_input()
        logger.info(f"Find and click window {title_re}")

def search_window(parent_window:WindowSpecification, title_re:str, control_type="", interval=2)-> WindowSpecification | None:
    """
    A foolish function- -
    find child window with parent_window,sleep 2 second and retry 3 times if failed
    because sometimes window is not loaded
    Args:
        parent_window (WindowSpecification):
        title_re (str):
        control_type (str):optional, not use if ""
        interval (int):optional
    Returns:
        child(WindowSpecification): if found,else return None


    """
    retry = 0
    while retry < 3:
        if control_type == "":
            child = (parent_window.child_window(title_re=title_re))
            child.wait('visible',timeout=10)
        else:
            child = (parent_window.child_window(title_re=title_re, control_type=control_type))
            child.wait('visible',timeout=10)
        if child is None:
            time.sleep(interval)
            retry += 1
            logger.warning(f"Can't find window:{title_re} from {parent_window.Window.__name__},retry")
        else:
            # 画个绿框
            child.draw_outline()
            return child
    logger.warning(f"Can't find window:{title_re} from {parent_window.Window.__name__} after retry 3 times")
    return None

def wechat_sign_in_and_get_password()->str:
    """
    在电脑上登录微信
    Return:今日密令，没获取到的话返回""
    """
    try:
        if not is_wechat_running():
            logger.info("Detect wechat is not running, try to start wechat")
            start_wechat()

        logger.info("Search wechat widget...")
        wechat_window = find_wechat_window()
        wechat_window.wait("visible",timeout=10)
        if wechat_window is None:
            logger.warning("WeChat widget not found, please check if it started successfully or if the path is correct.")
            return ""

        logger.info("Successfully find wechat widget")
        wechat_window.set_focus()
        logger.info("Set focus to wechat window")

        navi = search_window(wechat_window,title_re="导航")


        click_window(navi,title_re="通讯录",control_type="Button")

        gzh = search_window(wechat_window,title_re="公众号",control_type="ListItem")

        click_window(gzh,title_re="ContactListItem")

        click_window(wechat_window,title_re="忘川风华录手游",control_type="ListItem")



        gzh_info = find_wechat_app().window(title_re="公众号")
        time.sleep(2)
        click_window(gzh_info,title_re="发消息")


        find_gzh = findwindows.find_window(title_re="忘川风华录手游")
        app = Application('uia').connect(handle=find_gzh)
        gzh = app.window(handle=find_gzh)

        click_window(gzh,title_re="福利上门")

        click_window(gzh,title_re="每日签到", control_type="MenuItem")


        dialogList = gzh.child_window(title="消息", control_type="List")
        # 获取最后一条消息
        item = dialogList.children(control_type="ListItem")[-1]
        text = item.window_text()
        # 返回消息文本
        return handle_password_content(text)

    except Exception as e:
        print(e)
        return ""





# 读取注册表找到微信的安装路径  https://blog.csdn.net/capsclock/article/details/128374249
def getWxInstallPath()->str:
    try:
        # 注册表打开
        # RegOpenKey(key, subKey , reserved , sam)
        # key: HKEY_CLASSES_ROOT HKEY_CURRENT_USER HEKY_LOCAL_MACHINE HKEY_USERS HKEY_CURRENT_CONFIG
        # subkey: 要打开的子项
        # reserved: 必须为0
        # sam: 对打开的子项进行的操作,包括win32con.KEY_ALL_ACCESS、win32con.KEY_READ、win32con.KEY_WRITE等
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, "SOFTWARE\Tencent\WeChat", 0, win32con.KEY_ALL_ACCESS)
        # 这里的key表示键值，后面是具体的键名，读取出来是个tuple
        value = win32api.RegQueryValueEx(key, "InstallPath")[0]
        # 用完之后记得关闭
        win32api.RegCloseKey(key)
        # 微信的路径
        value += "\\" + "WeChat.exe"
        return value
    except Exception as ex:
        logger.warning(str(ex))

# 检查微信进程是否已经运行
def is_wechat_running():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'WeChat.exe':
            return True
    return False

def handle_password_content(input:str)->str:
    res = input.split("：")
    if len(res) != 2:
        return ""
    else:
        return res[-1]
# 启动微信
def start_wechat():
    wechat_path = getWxInstallPath()
    if not os.path.exists(wechat_path):
        raise FileNotFoundError(f"WeChat not found at {wechat_path}")
    app = Application('uia').start(wechat_path)

    # 查找并返回标题为“微信”的窗口
    dlg = app.window(title_re="微信")
    dlg.set_focus()
    # 打印登录界面窗口结构
    # dlg.print_control_identifiers()

    # 查找并返回标题为“进入微信”的按钮并点击
    but = click_window(dlg,title_re="进入微信", control_type="Button")
    # but = dlg.child_window()
    # but.click_input()

    # 等待登录加载



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

if __name__ == "__main__":
    wechat_sign_in_and_get_password()