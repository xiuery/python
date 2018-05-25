from task.Drop_Ship_PO_Process.page.Base_Page import BasePage
# from task.Drop_Ship_PO_Process.config.Base_Config import BaseConfig


class PoFulfillment(BasePage):

    def __init__(self, driver, logger):
        super(PoFulfillment, self).__init__(driver, logger)
        self.drop_ship_orders = []
        self.drop_ship_orders_fail = []
        self.drop_ship_orders_processed = []

    def drop_ship_order_process(self):
        self.logger.info('current window title: %s', self.driver.get_title())
        
        # 获取总页数,这里需要做个页数处理
        # count_string = self.driver.get_text('')

        # 寻找满足条件可以处理的order
        for order in self.get_drop_ship_orders():
            self.logger.info('order: %s', order)

            hour_aged = order['hours_aged']
            vendor_element = order['vendor_element']

            order.pop('vendor_element')
            order.pop('hours_aged')

            if order in self.drop_ship_orders:
                self.logger.info('order processed')
                continue

            # 无论是否成功的都需要保存的list中
            # 由于vendor_element不能deepcopy,只能删除之
            self.drop_ship_orders.append(order)

            if int(hour_aged) < 234:
                self.logger.info('drop ship order can be process')
                self.drop_ship_orders_processed.append(order)
                vendor_element.click()
                return True
            else:
                self.logger.info('no drop ship order can be process')
                self.drop_ship_orders_fail.append(order)
        return False

    def get_drop_ship_orders(self):
        """
        获取本页所有的order
        """
        self.logger.info('get drop ship orders')

        orders = []
        rows = self.driver.get_elements('xpath=>//*[@id="RI"]/tbody[1]/tr')

        if len(rows) <= 1:
            self.logger.info('no order, will exit')
            return orders

        for row in rows:
            columns = row.find_elements_by_xpath('.//td')
            order = {
                'buyer': columns[0].text.strip(),
                'vendor': columns[1].find_element_by_xpath('.//a[1]').text.strip(),
                'vendor_element': columns[1].find_element_by_xpath('.//a[1]'),
                'vendor_name': columns[2].text.strip(),
                'vpc': columns[3].find_element_by_xpath('.//a').text.strip(),
                'order_count': columns[4].text.strip(),
                'hours_aged': columns[5].text.strip()
            }
            orders.append(order)

        self.logger.info('orders: %s', orders)
        return orders
