import traceback
from base.utils.Log import drop_ship_po_process_logger as process_logger
from task.Drop_Ship_PO_Process.service.Vendor_Service import VendorService
from task.Drop_Ship_PO_Process.process.Order_Process import OrderProcess


class TaskHandler:

    def __init__(self):
        self.logger = process_logger

    def start(self):
        self.logger.info('Start process:')

        vendors = VendorService.get_vendors()
        for vendor in vendors:
            try:
                order_process = OrderProcess(self.logger)
                order_process.start(vendor)
                self.logger.info('Process success')
            except:
                traceback.print_exc()
                self.logger.info('Process failed')
            finally:
                pass

    def stop(self):
        self.logger.info('End process')
