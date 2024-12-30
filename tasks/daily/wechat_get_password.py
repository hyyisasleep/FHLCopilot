
import time
from module.exception import RequestHumanTakeover
from module.logger import logger
import os
import psutil
from pywinauto import Application, findwindows, WindowSpecification,timings,Desktop
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

    new:
    use wait()api and exists api
    Args:
        parent_window (WindowSpecification):
        title_re (str):
        control_type (str):optional, not use if ""
        interval (int):optional
    Returns:
        child(WindowSpecification): if found,else return None


    """
    timeout = 10
    retry = 0
    while retry < 3:
        if control_type == "":
            child = (parent_window.child_window(title_re=title_re))
            if not child.exists():
                child.wait('visible',timeout=timeout)
        else:
            child = (parent_window.child_window(title_re=title_re, control_type=control_type))
            if not child.exists():
                child.wait('visible',timeout=timeout)

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

def wechat_sign_in_and_get_password(config_wechat_path=r'D:\WeChat\WeChat.exe')->str:
    """
    在电脑上登录微信
    Return:今日密令，没获取到的话返回""
    """

    try:
        timings.Timings.fast()
        # 包括启动和在后台找微信主界面
        wechat_window = find_wechat_window(config_wechat_path)

        if wechat_window is None:
            return ""
        # 定位左侧边栏导航
        navi = search_window(wechat_window,title_re="导航")
        # 点击通讯录键 切换到通讯录界面
        click_window(navi,title_re="通讯录",control_type="Button")
        # 找联系人中公众号，应该不用划
        gzh = search_window(wechat_window,title_re="公众号",control_type="ListItem")
        # 按公众号键的真正按键ContactListItem
        click_window(gzh,title_re="ContactListItem")
        # 右边出现很多关注的公众号图标，点击焚化炉头像
        # ……应该不用划吧
        click_window(wechat_window,title_re="忘川风华录手游",control_type="ListItem")
        # 会开一个新的窗口，焚化炉公众号详情界面
        # TODO:
        gzh_info = find_wechat_app().window(title_re="公众号")
        # 详情界面会加载一会
        # 点详情界面的发消息键
        # TODO:发消息加载出来之后会往下挪一点导致点击失败
        click_window(gzh_info,title_re="发消息")
        # 新开窗口，发消息界面
        gzh_chat = find_wechat_app().window(title_re="忘川风华录手游")
        # 点击福利上门
        click_window(gzh_chat,title_re="福利上门")
        # 点击每日签到
        click_window(gzh_chat,title_re="每日签到", control_type="MenuItem")
        # 获取消息列表最后一条
        dialog_list = search_window(gzh_chat,title_re="消息", control_type="List")
        # 获取最后一条消息
        item = dialog_list.children(control_type="ListItem")[-1]
        text = item.window_text()
        # 返回筛选后的密令
        return handle_password_content(text)

    except Exception as e:
        print(e)
        return ""


def handle_password_content(input:str)->str:
    res = input.split("：")
    if len(res) != 2:
        return ""
    else:
        return res[-1]


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
        return ""

# 检查微信进程是否已经运行
def is_wechat_running():
    wechat_pid = None
    for process in psutil.process_iter(['pid','name']):
        if process.info['name'] == 'WeChat.exe':
            wechat_pid = process.info['pid']
            break
    return wechat_pid


# 启动微信
def start_wechat(wechat_path_list):

    """
    Args:
        wechat_path_list (list):  [register_path,config_path(manual)]
    """
    wechat_path = wechat_path_list[0]
    if not os.path.exists(wechat_path):
        if os.path.exists(wechat_path_list[1]):
            wechat_path = wechat_path_list[1]
        else:
            logger.warning(f"Can't find wechat automatically or by config path: {wechat_path}, please modify config path")
            raise RequestHumanTakeover
    app = Application('uia').start(wechat_path)

    # 查找并返回标题为“微信”的窗口
    dlg = app.window(title_re="微信")
    if not dlg.exists():
        dlg.wait("visible")
    dlg.set_focus()
    # 打印登录界面窗口结构
    # dlg.print_control_identifiers()

    # 查找并返回标题为“进入微信”的按钮并点击
    click_window(dlg,title_re="进入微信", control_type="Button")


    # 等待登陆加载，但是用能找到导航栏作为登陆成功标志
    # 理论上下面的dlg和上面的不是一个但它们既然同名也能跑就凑合用了
    search_window(dlg, title_re="导航")
    logger.info("Successful start wechat app")
    return app

def find_wechat_app():
    try:
        wechat_window = findwindows.find_window(title_re="微信")
        app = Application('uia').connect(handle=wechat_window)
        return app
    except Exception as e:
        print(e)
        return None
# 获取微信窗口
def find_wechat_window(config_wechat_path)->WindowSpecification | None:
    try:
        wechat_path = [getWxInstallPath(),config_wechat_path]
        # 启动微信

        wechat_pid = is_wechat_running()
        if wechat_pid is None:
            logger.info("Detect wechat is not running, try to start wechat")
            app = start_wechat(wechat_path)
        else:
            logger.info("Detect wechat is running, try to open widget")
            app = Application('uia').connect(process=wechat_pid)
        # 有微信进程但是在后台，重新启动一次把窗口招出来
        # logger.info("Search wechat widget...")
        #
        # try:
        #     findwindows.find_window(title_re="微信")
        # except WindowNotFoundError as e:
        #     logger.info("Detect WeChat widget is not open, try to open it")
        #     app = Application('uia').start(wechat_path_list)

        # 获取微信窗口
        # wechat_window = Desktop(backend="uia").window(title="微信")
        # wechat_window.restore()  # 恢复最小化
        # wechat_window.set_focus()  # 将窗口置于前台

        # wechat_window = findwindows.find_window(title_re="微信")
        # app = Application('uia').connect(handle=wechat_window)
        if app is None:
            logger.warning("Fail to connect wechat")
            return None

        wechat_window = app.window(title_re="微信")
        #
        if not wechat_window.exists():
            wechat_window.restore()
            wechat_window.wait("visible")
        logger.info("Set focus to wechat widget")
        wechat_window.set_focus()

        if wechat_window is None:
            logger.warning(
                "WeChat widget not found, please check if it started successfully or if the path is correct.")
            return None

        logger.info("Successfully find wechat widget")
        return wechat_window

    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    wechat_sign_in_and_get_password()