from task.Drop_Ship_PO_Process.page.Base_Page import BasePage


class DropShipOrder(BasePage):
    def __init__(self, driver, logger):
        super(DropShipOrder, self).__init__(driver, logger)
        self.columns = ['PM Code', 'Vend No', 'MSO#', 'Inv Type',
                       'Cust PO#', 'Part No', 'ABC Code', 'MSO Order Qty',
                       'Aging by Hour', 'Comment', 'Contact']
        self.drop_ship_orders_detail = []

    def process(self):
        self.logger.info('current window title: %s', self.driver.get_title())
        self.logger.info('location to drop ship order detail')

        # 检查表头是否变化
        self.logger.info('check column whether change or not')
        if self.column_must_have() is False:
            self.logger.info('column changed')
            raise

        self.get_drop_ship_order_detail()
        self.driver.go_back()
        # self.driver.F5()

    def get_drop_ship_order_detail(self):
        """
        获取表格数据
        """
        self.logger.info('get drop ship order detail')

        rows = self.driver.get_elements('xpath=>//*[@id="RI"]/tbody/tr')
        for row in rows:
            columns = row.find_elements_by_xpath('.//td')
            order_detail = {
                'pm_code': columns[0].text,
                'vendor': columns[1].text,
                'mso': columns[2].find_element_by_xpath('.//a').text,
                'inv_type': columns[3].text,
                'cust_po': columns[4].text,
                'part_no': columns[5].find_element_by_xpath('.//a').text,
                'abc_code': columns[6].text,
                'mso_order_qty': columns[7].text,
                'aging_by_hour': columns[8].text
            }
            # 获取mso详情
            columns[2].find_element_by_xpath('.//a').click()
            order_detail['mso_detail'] = self.get_mso_detail()

            self.drop_ship_orders_detail.append(order_detail)

    def get_mso_detail(self):
        self.logger.info('get mso detail')

        mso_detail = {}

        # 切换到mso详情页面
        self.driver.switch_to_window_by_index(1)
        self.driver.max_window()
        self.logger.info('current window title: %s', self.driver.get_title())

        mso_detail['ship_method'] = self.driver.get_text('xpath=>//*[@id="warp"]/div/div/div[2]/section[2]/table/tbody/tr[1]/td')
        mso_detail['freight'] = self.driver.get_text('xpath=>//*[@id="warp"]/div/div/div[2]/section[2]/table/tbody/tr[2]/td[1]/span')
        mso_detail['freight_1'] = self.driver.get_text('xpath=>//*[@id="warp"]/div/div/div[2]/section[2]/table/tbody/tr[2]/td[2]/span')
        mso_detail['ref_no'] = self.driver.get_text('xpath=>//*[@id="warp"]/div/div/div[2]/section[2]/table/tbody/tr[3]/td/a')
        self.driver.close()
        self.driver.switch_to_window_by_index(0)

        return mso_detail

    def column_must_have(self):
        """
        因为在这个页面表头是可以设置的,因此必须校验必须要有的表头
        column增加或者减少都会造成数据错位
        """
        columns = self.driver.get_elements('xpath=>//*[@id="RI"]/thead/tr/th')

        if columns[0].text.strip() == self.columns[0] \
                and columns[1].text.strip() == self.columns[1] \
                and columns[2].text.strip() == self.columns[2] \
                and columns[3].text.strip() == self.columns[3] \
                and columns[4].text.strip() == self.columns[4] \
                and columns[5].text.strip() == self.columns[5] \
                and columns[6].text.strip() == self.columns[6] \
                and columns[7].text.strip() == self.columns[7] \
                and columns[8].text.strip() == self.columns[8] \
                and columns[9].text.strip() == self.columns[9] \
                and columns[10].text.strip() == self.columns[10]:

            return True
        else:
            return False

