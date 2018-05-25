from task.Drop_Ship_PO_Process.process.Base_Process import BaseProcess


class OrderProcess(BaseProcess):
    def __init__(self, logger):
        super(OrderProcess, self).__init__(logger)

    def execute(self):

        while True:
            process = self.po_fulfillment.drop_ship_order_process()

            print(self.po_fulfillment.drop_ship_orders)
            print(self.po_fulfillment.drop_ship_orders_fail)
            print(self.po_fulfillment.drop_ship_orders_processed)

            # 检测到有order才继续执行
            if process is True:
                self.drop_ship_order.process()
                print(self.drop_ship_order.drop_ship_orders_detail)
            else:
                break
