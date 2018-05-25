
"""
测试关于需要验证码登录的网站
通过事先登录过的机器上，程序启动浏览器时加载用户数据
"""

from py_xs.XiuerySelenium import XiuerySelenium


class LoginCaptchaWebsite(XiuerySelenium):

    def __init__(self, element, browser, user_data=''):
        super(LoginCaptchaWebsite, self).__init__(browser, user_data)
        self.element = element

    def login(self, username, password):
        self.open(self.element['url'])
        self.max_window()
        print(self.driver.get_cookies())
        self.click(self.element['account_login'])
        self.clear(self.element['username'])
        self.type(self.element['username'], username)
        self.clear(self.element['password'])
        self.type(self.element['password'], password)
        self.click(self.element['submit'])


if __name__ == '__main__':

    import time
    import traceback

    user_data_dir = 'C:\\Users\\next\\AppData\\Local\\Google\\Chrome\\User Data\\Default'

    elements = {
        'url': 'https://passport.jd.com/uc/login',
        'account_login': 'xpath=>//*[@id="content"]/div[2]/div[1]/div/div[3]/a',
        'username': 'id=>loginname',
        'password': 'id=>nloginpwd',
        'submit': 'id=>loginsubmit'
    }

    login_captcha_website = LoginCaptchaWebsite(elements, 'chrome_user_data', user_data_dir)
    try:
        login_captcha_website.login(username='', password='')
    except:
        traceback.print_exc()
    finally:
        time.sleep(10)
        login_captcha_website.quit()
