# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from bs4 import BeautifulSoup
import random
import time
import requests
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse, Response
class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        print('代理')
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
        #request.meta['proxy'] = 'http://112.90.133.253'
    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        print("\n出现异常，正在使用代理重试....\n")
        #request.meta['proxy'] = 'http://112.90.133.253'
        #return request
class myProxy(object):

    def process_request(self,request,spider):
        proxy=requests.get("http://127.0.0.1:5010/get").text
        request.meta['proxy']='http://'+proxy
        
    def process_response(self, request, response, spider):
        response.status = 204
        return response


class ProxyMiddleware(object):
    '''
    设置Proxy
    '''

    def __init__(self, ip):
        self.ip = ip

    @classmethod
    def from_crawler(cls, crawler):
        return cls(ip=crawler.settings.get('PROXIES'))

    def process_request(self, request, spider):
        ip = random.choice(self.ip)
        request.meta['proxy'] = ip
class MoveSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MoveDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
class MoveDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
class SeleniumMiddleware(object):
    def __init__(self,timeout=5):
        pass

        #chrome_options = Options()
        # prefs = {
        #     'profile.default_content_setting_values': {
        #         'images': 2,  # 禁用图片的加载
        #         #'javascript': 2  # 禁用js，可能会导致通过js加载的互动数抓取失效
        #     }
        # }
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_experimental_option("prefs", prefs)
        # self.browser = webdriver.Chrome()
        # self.timeout = timeout
        # self.browser.maximize_window()
        # # self.browser.implicitly_wait(20)
        # # self.browser.set_page_load_timeout(25)
        # self.browser.set_page_load_timeout(self.timeout)
        # self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        pass
        #self.browser.close()

    def process_request(self, request, spider):
        if spider.name == "toutiao":
            content = self.selenium_request(request.url);
            if content.strip() != '':
                print(11212121212121)
                return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
            return None
            # return None
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
        else:
            pass

    def selenium_request(self, url):
        # js控制浏览器滚动到底部js
        js = """
        function scrollToBottom() {
            var Height = document.body.clientHeight,  //文本高度
                screenHeight = window.innerHeight,  //屏幕高度
                INTERVAL = 100,  // 滚动动作之间的间隔时间
                delta = 500,  //每次滚动距离
                curScrollTop = 0;    //当前window.scrollTop 值
            console.info(Height)
            var scroll = function () {
                //curScrollTop = document.body.scrollTop;
                curScrollTop = curScrollTop + delta;
                window.scrollTo(0,curScrollTop);
                console.info("偏移量:"+delta)
                console.info("当前位置:"+curScrollTop)
            };
            var timer = setInterval(function () {
                var curHeight = curScrollTop + screenHeight;
                if (curHeight >= Height){   //滚动到页面底部时，结束滚动
                    clearInterval(timer);
                }
                scroll();
            }, INTERVAL)
        };
        scrollToBottom()
        """
        time.sleep(5)

        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,  # 禁用图片的加载
                #'javascript': 2  # 禁用js，可能会导致通过js加载的互动数抓取失效
            }
        }

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs", prefs)
        # headless无界面模式
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
        #prefs = {"profile.managed_default_content_settings.images": 2}
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path="C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python36\\Scripts\\chromedriver")

        time.sleep(5)
        driver.get(url)
        time.sleep(5)
        driver.maximize_window();# 窗口最大化
        # 执行js滚动浏览器窗口到底部
        driver.execute_script(js)
        time.sleep(5)  # 不加载图片的话，这个时间可以不要，等待JS执行
        # driver.get_screenshot_as_file("C:\\Users\\Administrator\\Desktop\\test.png")
        content = driver.page_source.encode('utf-8')
        # iframe = driver.find_elements_by_tag_name('iframe')[2]
        # driver.switch_to.frame(iframe)  # 最重要的一步
        # content = BeautifulSoup(driver.page_source, "html.parser")
        driver.switch_to.frame('player-frame')  # frame括号里面的是它的id
        trs = driver.find_elements_by_tag_name('div')
        print(trs)
        #print(content)
        #print(content)
        # driver.quit()
        #driver.close()
        # return None
        return content