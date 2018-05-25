from task.Drop_Ship_PO_Process.login.Central_Login import CentralLogin
from task.Drop_Ship_PO_Process.page.Po_Fulfillment import PoFulfillment
from task.Drop_Ship_PO_Process.page.Drop_Ship_Order import DropShipOrder


class BaseProcess(object):

    def __init__(self, logger):
        self.data = None
        self.logger = logger
        self.driver = None
        self.po_fulfillment = None
        self.drop_ship_order = None

    def start(self, vendor):
        login_central = CentralLogin(vendor, self.logger)
        self.driver = login_central.driver

        self.po_fulfillment = PoFulfillment(self.driver, self.logger)
        self.drop_ship_order = DropShipOrder(self.driver, self.logger)
        try:
            login_central.login_central()
            self.execute()
            return self.data
        finally:
            self.logger.info('close browser...')
            self.driver.quit()

    def execute(self):
        return False
