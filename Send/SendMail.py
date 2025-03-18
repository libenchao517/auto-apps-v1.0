################################################################################
# 本文件用于自动发送邮件的实现
################################################################################
# 导入模块
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .config import Send_config
config = Send_config()
################################################################################
# 自动发送类
class Auto_Email:
    def __init__(self, subject):
        """
        初始化
        :param subject: 邮件主题
        """
        # 服务器
        self.mail_host = config.mail_host
        # 发送者邮箱号
        self.mail_sender = config.mail_sender
        # 发送者邮箱密码
        self.mail_passwd = config.mail_passwd
        # 接收者邮箱号
        self.mail_to = config.mail_to
        self.subject = subject

    def Send(self, msg):
        """
        配置邮件
        :param msg: 发送的内容
        :return: None
        """
        s = smtplib.SMTP()
        s.connect(self.mail_host, 25)
        s.login(self.mail_sender, self.mail_passwd)
        s.sendmail(self.mail_sender, self.mail_to, msg.as_string())
        s.quit()

    def Send_txt(self, txt):
        """
        只发送文字的情况
        :param txt: 发送的文本
        :return: None
        """
        msg = MIMEText(txt, 'plain', 'utf-8')
        msg["Subject"] = self.subject
        msg["From"] = self.mail_sender
        msg["To"] = self.mail_to
        self.Send(msg)

    def Send_picture(self, txt, filename):
        """
        发送图片的情况
        :param txt: 发送的文本
        :param filename: 文件名列表
        :return: None
        """
        msg = MIMEMultipart()
        msg["Subject"] = self.subject
        msg["From"] = self.mail_sender
        msg["To"] = self.mail_to
        content = txt
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        for pic in filename:
            jpgpart = MIMEApplication(open(pic, 'rb').read())
            jpgpart.add_header('Content-Disposition', 'attachment', filename=pic)
            msg.attach(jpgpart)
        self.Send(msg)
