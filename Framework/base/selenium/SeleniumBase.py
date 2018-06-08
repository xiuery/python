# -*- coding: utf-8 -*-
__author__ = 'Colin Wang'

from selenium import webdriver
from func_timeout import func_set_timeout
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from pyse.pyse_api import WebDriver, ActionChains, By, WebDriverWait, EC, NoSuchElementException


class SeleniumBase(WebDriver):
    """
    Run class initialization method, the default is proper
    to drive the Firefox browser. Of course, you can also
    pass parameter for other browser, Chrome browser for the "Chrome",
    the Internet Explorer browser for "internet explorer" or "ie".
    """
    def __init__(self, browser='ie'):
        if browser == "ff":
            self.driver = webdriver.Firefox()
        elif browser == "ff_headless":
            ff_options = FirefoxOptions()
            ff_options.set_headless()
            self.driver = webdriver.Firefox(firefox_options=ff_options)
        elif browser == "chrome":
            self.driver = webdriver.Chrome()
        elif browser == "internet explorer" or browser == "ie":
            self.driver = webdriver.Ie()
        elif browser == "opera":
            self.driver = webdriver.Opera()
        elif browser == "chrome_headless":
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        elif browser == 'edge':
            self.driver = webdriver.Edge()
        else:
            raise NameError("Not found %s browser,You can enter 'ie', 'ff', 'opera', 'edge', 'chrome' or 'chrome_headless'." % browser)

    '''
    切换回主窗口
    '''
    def switch_to_main_window(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    def switch_to_window_by_index(self, index):
        self.driver.switch_to.window(self.driver.window_handles[index])

    '''
    返回上一页
    '''
    def go_back(self):
        self.driver.back()

    '''
    鼠标右键
    '''
    def context_click(self, element):
        ActionChains(self.driver).context_click(element).perform()

    '''
    显示等待alert
    '''
    def alert_wait(self, secs=30):
        WebDriverWait(self.driver, secs, 1).until(EC.alert_is_present())

    '''
    wait 
    '''
    @func_set_timeout(30)
    def wait_window_by_title(self, title):
        '''
        Use the window title select window.

        Usage:
        driver.wait_window_by_title("window title")
        '''
        while True:
            all_handles = self.driver.window_handles
            for handle in all_handles:
                self.driver.switch_to.window(handle)
                if self.driver.title == title:
                    return True

    '''
    wait 
    '''
    @func_set_timeout(30)
    def wait_window_by_titles(self, titles):
        '''
        Use the window title select window.

        Usage:
        driver.wait_window_by_title("window title")
        '''
        while True:
            all_handles = self.driver.window_handles
            for handle in all_handles:
                self.driver.switch_to.window(handle)
                if self.driver.title in titles:
                    return True

    '''
    显示等待元素节点
    '''
    def element_wait(self, by, value, secs=30):
        '''
        Waiting for an element to display.
        '''
        if by == "id":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.ID, value)))
        elif by == "name":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.NAME, value)))
        elif by == "class":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
        elif by == "link_text":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
        elif by == "xpath":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.XPATH, value)))
        elif by == "css":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
        else:
            raise NoSuchElementException("Not find element, Please check the syntax error.")

    '''
    显示等待元素visible
    '''
    def element_visible_wait(self, by, value, secs=30):
        '''
        Waiting for an element to visible.
        '''
        if by == "id":
            WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.ID, value)))
        elif by == "name":
            WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.NAME, value)))
        elif by == "class":
            WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, value)))
        elif by == "link_text":
            WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, value)))
        elif by == "xpath":
            WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.XPATH, value)))
        elif by == "css":
            WebDriverWait(self.driver, secs, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, value)))
        else:
            raise NoSuchElementException("Not find element, Please check the syntax error.")

    def get_element_visible(self, css):
        '''
        Judge element positioning way, and returns the element.
        '''
        if "=>" not in css:
            by = "css"
            value = css
            # wait element.
            self.element_visible_wait(by, css)
        else:
            by = css.split("=>")[0]
            value = css.split("=>")[1]
            if by == "" or value == "":
                raise NameError("Grammatical errors,reference: 'id=>useranme'.")
            self.element_visible_wait(by, value)

        if by == "id":
            element = self.driver.find_element_by_id(value)
        elif by == "name":
            element = self.driver.find_element_by_name(value)
        elif by == "class":
            element = self.driver.find_element_by_class_name(value)
        elif by == "link_text":
            element = self.driver.find_element_by_link_text(value)
        elif by == "xpath":
            element = self.driver.find_element_by_xpath(value)
        elif by == "css":
            element = self.driver.find_element_by_css_selector(value)
        else:
            raise NameError(
                "Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
        return element

    def get_elements(self, css):
        '''
        Judge element positioning way, and returns the element.
        '''
        if "=>" not in css:
            by = "css"
            value = css
            # wait element.
            self.element_wait(by, css)
        else:
            by = css.split("=>")[0]
            value = css.split("=>")[1]
            if by == "" or value == "":
                raise NameError("Grammatical errors,reference: 'id=>useranme'.")
            self.element_wait(by, value)

        if by == "id":
            elements = self.driver.find_elements_by_id(value)
        elif by == "name":
            elements = self.driver.find_elements_by_name(value)
        elif by == "class":
            elements = self.driver.find_elements_by_class_name(value)
        elif by == "link_text":
            elements = self.driver.find_elements_by_link_text(value)
        elif by == "xpath":
            elements = self.driver.find_elements_by_xpath(value)
        elif by == "css":
            elements = self.driver.find_elements_by_css_selector(value)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpath','css'.")
        return elements

