# -*- coding: utf-8 -*-
__author__ = 'Kerwin zhang'
import sys
sys.path.append("..\..")
import time
from base.selenium.Selenium_Base import Selenium_Base

'''
    temporary data
'''
central_username_element = "id=>j_username"
central_passwd_element = "id=>j_password"
central_login_button_element = "xpath=>//input[@id='login']"
central_sso_login_button_element = "xpath=>//input[@value='Login by SSO']"
central_search_element = "id=>searchMenuInp"
############################


class Synnexcentral(Selenium_Base):

    def __init__(self, driver, logger):
        self.driver = driver
        super(Synnexcentral, self).__init__(logger)

    def login_central(self, central_url, central_username, central_pwd, ssologin=True):
        '''
        :param ssologin: if want to login as sso, pls use it as 'login_central(False)'
        :return:
        '''
        #visit synnex central
        self.open(central_url)
        self.max_window()
        if ssologin:
            #Login the central
            self.clear(central_username_element)
            self.type(central_username_element, central_username)
            self.clear(central_passwd_element)
            self.type(central_passwd_element, central_pwd)
            #self.click(central_login_button_element)
            self.simulate_enter(central_passwd_element)
            return self.get_title()
        else:
            self.type(central_sso_login_button_element)
            return self.get_title()

    def enter_business_page(self, business_name):
        '''
        :param business_name: which business web page you want to visit
        :return:
        '''
        self.clear(central_search_element)
        self.type(central_search_element, business_name)
        time.sleep(5)
        self.simulate_enter(central_search_element)
        time.sleep(10)
        self.swith_new_window()
        return self.get_title()


if __name__ == '__main__':
    from selenium import webdriver
    from base.utils.Log import edi_oc_ca_walmart_logger
    driver = webdriver.Ie()

    central = Synnexcentral(driver,edi_oc_ca_walmart_logger)
    central.login_central('www.baidu.com','1','2',False)
