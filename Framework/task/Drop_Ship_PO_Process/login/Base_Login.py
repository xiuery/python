from base.selenium.SeleniumBase import SeleniumBase
from task.Drop_Ship_PO_Process.config.Base_Config import BaseConfig


class BaseLogin(object):
    def __init__(self, vendor, logger):
        self.vendor = vendor
        self.logger = logger
        self.driver = SeleniumBase(self.get_browser())

    def login_central(self):
        self.logger.info("Login SYNNEX Central, url: %s", self.get_url())
        self.driver.open(self.get_url())
        self.driver.switch_to_main_window()
        self.logger.info("input username: %s", BaseConfig.get_value('username'))
        self.logger.info("input username: %s", self.get_username())
        self.driver.type(BaseConfig.get_value('username'), self.get_username())
        self.logger.info("input password: %s", BaseConfig.get_value('password'))
        self.driver.type(BaseConfig.get_value('password'), self.get_password())
        self.logger.info("click login button: %s", BaseConfig.get_value('login'))
        self.driver.submit(BaseConfig.get_value('login'))
        self.logger.info('login success')

        self.logger.info('wait cis main menu load, titles: %s', self.get_central_titles())
        self.driver.wait_window_by_titles(self.get_central_titles())

        self.go_to_business()

    def get_url(self):
        pass

    def get_browser(self):
        pass

    def get_username(self):
        pass

    def get_password(self):
        pass

    def get_central_titles(self):
        pass

    def go_to_business(self):
        pass
