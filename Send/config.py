################################################################################
# 自动发送邮件模块的配置文件
################################################################################
# 导入必要模块
class Send_config:
    def __init__(self):
        # 服务器
        self.mail_host = "smtp.sina.com"
        # 发送者邮箱号
        self.mail_sender = "yourname@sina.com"
        # 发送者邮箱密码
        self.mail_passwd = "yourpassword"
        # 接收者邮箱号
        self.mail_to = "yourname@126.com"

