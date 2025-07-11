"""
This file stores server, such as 'cn', 'en'.
Use 'import module.config.server as server' to import, don't use 'from xxx import xxx'.
"""
lang = 'cn'  # Setting default to cn, will avoid errors when using dev_tools
server = 'CN-Official'

VALID_LANG = ['cn', 'en']
VALID_SERVER = {
    'CN-Official': 'com.netease.pm03',
    # ,
    'CN-Bilibili': 'com.netease.pm03.bilibili',
    'CN-Vivo':  'com.netease.pm03.vivo',
    'CN-Oppo':  'com.netease.pm03.nearme.gamecenter',
    'CN-Huawei':  'com.netease.pm03.huawei',
    'CN-Xiaomi': 'com.netease.pm03.mi'
    # 'OVERSEA-America': 'com.HoYoverse.hkrpgoversea',
    # 'OVERSEA-Asia': 'com.HoYoverse.hkrpgoversea',
    # 'OVERSEA-Europe': 'com.HoYoverse.hkrpgoversea',
    # 'OVERSEA-TWHKMO': 'com.HoYoverse.hkrpgoversea',
}
VALID_PACKAGE = set(list(VALID_SERVER.values()))
VALID_CLOUD_SERVER = {
    'CN-Official': 'com.miHoYo.cloudgames.hkrpg',
}
VALID_CLOUD_PACKAGE = set(list(VALID_CLOUD_SERVER.values()))

DICT_PACKAGE_TO_ACTIVITY = {
    'com.netease.pm03': 'com.netease.ntunisdk.external.protocol.ProtocolLauncher',
    'com.netease.pm03.bilibili': 'com.netease.ntunisdk.external.protocol.ProtocolLauncher',
    'com.netease.pm03.vivo': 'com.netease.ntunisdk.external.protocol.ProtocolLauncher',
    'com.netease.pm03.nearme.gamecenter': 'com.netease.ntunisdk.external.protocol.ProtocolLauncher',
    'com.netease.pm03.huawei': 'com.netease.ntunisdk.external.protocol.ProtocolLauncher',
    'com.netease.pm03.mi':'com.netease.ntunisdk.external.protocol.ProtocolLauncher'
    # 'com.HoYoverse.hkrpgoversea': 'com.mihoyo.combosdk.ComboSDKActivity',
    # 'com.miHoYo.cloudgames.hkrpg': 'com.mihoyo.cloudgame.ui.SplashActivity',
}


def set_lang(lang_: str):
    """
    Change language and this will affect globally,
    including assets and language specific methods.

    Args:
        lang_: package name or server.
    """
    global lang
    lang = lang_

    from module.base.resource import release_resources
    release_resources()


def to_server(package_or_server: str) -> str:
    """
    Convert package/server to server.
    To unknown packages, consider they are a CN channel servers.
    """
    # Can't distinguish different regions of oversea servers,
    # assume it's 'OVERSEA-Asia'
    if package_or_server == 'com.HoYoverse.hkrpgoversea':
        return 'OVERSEA-Asia'

    for key, value in VALID_SERVER.items():
        if value == package_or_server:
            return key
        if key == package_or_server:
            return key
    for key, value in VALID_CLOUD_SERVER.items():
        if value == package_or_server:
            return key
        if key == package_or_server:
            return key

    raise ValueError(f'Package invalid: {package_or_server}')


def to_package(package_or_server: str, is_cloud=False) -> str:
    """
    Convert package/server to package.
    """
    if is_cloud:
        for key, value in VALID_CLOUD_SERVER.items():
            if value == package_or_server:
                return value
            if key == package_or_server:
                return value
    else:
        for key, value in VALID_SERVER.items():
            if value == package_or_server:
                return value
            if key == package_or_server:
                return value

    raise ValueError(f'Server invalid: {package_or_server}')
