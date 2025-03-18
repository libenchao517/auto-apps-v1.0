################################################################################
# 本文件用于邮件发送中的关键函数
################################################################################
# 导入模块
import requests
################################################################################
def check_Internet(lock = False):
    """
    检查网络状况
    :param lock: 是否关闭邮件发送功能
    :return: 网络是否畅通
    """
    if lock:
        return False
    try:
        Webconnect = requests.get("https://www.baidu.com")
        if Webconnect.status_code == 200:
            Internet=True
        else:
            Internet = False
    except:
        Internet = False
    return Internet
