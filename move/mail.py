import scrapy
from scrapy.mail import MailSender
from move import settings

class Mail():
    def send(object,to, subject, body):
        mailer = MailSender(smtphost=settings.MAIL_HOST,  # 发送邮件的服务器
                            mailfrom=settings.MAIL_FROM,  # 邮件发送者
                            smtpuser=settings.MAIL_USER,  # 用户名
                            smtppass=settings.MAIL_PASS,  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
                            smtpport=settings.MAIL_PORT  # 端口号
                            )
        try:

            mailer.send(to,subject, body)

        except :

            pass
        pass

