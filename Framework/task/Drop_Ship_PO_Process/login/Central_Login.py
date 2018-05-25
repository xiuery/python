import time
from task.Drop_Ship_PO_Process.login.Base_Login import BaseLogin
from task.Drop_Ship_PO_Process.config.Base_Config import BaseConfig


class CentralLogin(BaseLogin):
    def __init__(self, vendor, logger):
        self.logger = logger
        super(CentralLogin, self).__init__(vendor, logger)

    def get_url(self):
        return self.vendor.url

    def get_browser(self):
        return self.vendor.browser.lower()

    def get_username(self):
        return self.vendor.username

    def get_password(self):
        return self.vendor.password

    def get_central_titles(self):
        central_title = 'Synnex Central@fca-vm-uat-jboss6-mycis-g1i1.synnex.org,'
        central_title += 'Synnex Central@fca-vm-uat-jboss6-mycis-g1i2.synnex.org,'
        central_title += 'Synnex Central@fca-vm-uat-jboss6-mycis-g1i3.synnex.org,'
        central_title += 'Synnex Central@fca-vm-uat-jboss6-mycis-g1i4.synnex.org,'
        central_title += 'Synnex Central@fca-vm-uat-jboss6-mycis-g1i5.synnex.org,'
        central_title += 'Synnex Central@fca-vm-uat-jboss6-mycis-g1i6.synnex.org,'
        central_title += 'Synnex Central@fca-vm-uat-jboss6-mycis-g1i7.synnex.org'
        return central_title.split(',')

    def go_to_business(self):
        self.logger.info('current window title: %s', self.driver.get_title())

        # 测试附加流程：切换权限
        self.logger.info('测试附加流程')
        self.logger.info('用户头像菜单')
        self.driver.click('xpath=>//*[@id="accountPlace"]/li/a/label')
        self.logger.info('切换到Super权限')
        self.driver.click('xpath=>//*[@id="userDnaRoles"]/li[3]')
        self.logger.info('测试附加流程 END')

        self.logger.info('reports menu: %s', BaseConfig.get_value('reports_menu'))
        self.driver.click(BaseConfig.get_value('reports_menu'))
        self.logger.info('po fulfillment - drop ship: %s', BaseConfig.get_value('po_fulfillment'))
        self.driver.click(BaseConfig.get_value('po_fulfillment'))

        # 测试流程
        self.logger.info('测试流程')
        self.logger.info('close mycis, and switch to window: po fulfillment - drop ship')
        self.driver.close()
        time.sleep(1)
        self.driver.switch_to_window_by_index(0)
        self.logger.info('current window title: %s', self.driver.get_title())
        self.driver.max_window()
        self.driver.click('xpath=>//*[@id="RI"]/tbody[1]/tr/td[1]/a')
        self.logger.info('测试流程 END')
