
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

def search_window(father_window:WindowSpecification,title_re:str,control_type="",interval=2)->WindowSpecification:
    """
    A foolish function- -
    find child window with father_window,sleep 2 second and retry 3 times if failed
    because sometimes window is not loaded
    Args:
        father_window (WindowSpecification):
        title_re (str):
        control_type (str):optional, not use if ""
        interval (int):optional
    Returns:
        child(WindowSpecification): if found,else return None


    """
    retry = 0
    while retry < 3:
        if control_type == "":
            child = father_window.child_window(title_re=title_re)
        else:
            child = father_window.child_window(title_re=title_re, control_type=control_type)
        if child is None:
            time.sleep(interval)
            retry += 1
        else:
            return child
    logger.warning(f"Can't find window:{title_re} from {father_window.Window.__name__} after retry 3 times")
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
        if wechat_window is None:
            logger.warning("WeChat widget not found, please check if it started successfully or if the path is correct.")
            return ""

        logger.info("Successfully find wechat widget")
        wechat_window.set_focus()

        # navi = wechat_window.child_window(title_re="导航")
        # if navi is None:
        #     logger.info("Can't find navi button,retry")
        navi = search_window(wechat_window,title_re="导航")


        click_window(navi,title_re="通讯录",control_type="Button")
        # address_book = search_window(navi,title_re="通讯录",control_type="Button")
        # address_book.click_input()
        # logger.info("Click address book button")

        gzh = search_window(wechat_window,title_re="公众号",control_type="ListItem")
        # gzh = wechat_window.child_window()
        # if gzh is None:
        #     print("找不到公众号")

        click_window(gzh,title_re="ContactListItem")
        # gzh = gzh.child_window()
        # gzh.click_input()
        # print("切换到公众号界面")

        click_window(wechat_window,title_re="忘川风华录手游",control_type="ListItem")
        # fhl = wechat_window.child_window(title_re="忘川风华录手游",control_type="ListItem")
        # if fhl is None:
        #     print("没找到手游公众号")
        # fhl.click_input()
        # print("进入风华录公众号")

        time.sleep(2)
        # 进入公众号消息界面

        gzh_info = find_wechat_app().window(title_re="公众号")
        click_window(gzh_info,title_re="发消息")

        print("打开公众号消息界面")
        find_gzh = findwindows.find_window(title_re="忘川风华录手游")
        app = Application('uia').connect(handle=find_gzh)
        gzh = app.window(handle=find_gzh)

        click_window(gzh,title_re="福利上门")
        # but = gzh.child_window()
        # but.click_input()
        # print("点击福利上门按钮")
        click_window(gzh,title_re="每日签到", control_type="MenuItem")
        # print("打开每日签到界面")

        time.sleep(1)
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

