import scrapy
from scrapy.mail import MailSender
from move import settings
from move.mail import Mail



class Spider(scrapy.Spider):
    """
    name = 'ip'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    def parse(self,response):
        print(response.text)
        print('\n')
        print(response.status)
    """
    name = 'mail'
    start_urls = ['http://baidu.com']

    def parse(self, response):
        """
        mailer = MailSender(smtphost=settings.MAIL_HOST,  # 发送邮件的服务器
                mailfrom=settings.MAIL_FROM,   # 邮件发送者
                smtpuser=settings.MAIL_USER,   # 用户名
                smtppass=settings.MAIL_PASS,  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
                smtpport=settings.MAIL_PORT  # 端口号
        )
        to='673541264@qq.com'
        body = '''
                    抓取了50页百思不得姐的段子，请详细查看数据库%s

                    此邮件由系统自动发送，请勿回复。
                    '''%(to)
        mailer.send(to,'抓取了50页段子',body)
        """
        MailSender=Mail()
        to = '673541264@qq.com'
        subject = '673541264@qq.com'
        body = '''
                                        抓取了50页百思不得姐的段子，请详细查看数据库%s

                                        此邮件由系统自动发送，请勿回复。
                                        ''' % (to)
        MailSender.send(to, subject, body)


