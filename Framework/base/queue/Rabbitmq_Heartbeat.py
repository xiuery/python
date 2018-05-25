
import time
import threading

heartbeat = 60


class RabbitMQHeartbeat(threading.Thread):
    """
    MQ的心跳线程
    """
    def __init__(self, connection):
        """
        :param connection: RabbitMQ的连接对象
        """
        super(RabbitMQHeartbeat, self).__init__()
        self.lock = threading.Lock()
        self.connection = connection
        self.quit_flag = False
        self.stop_flag = True
        self.setDaemon(True)

    def run(self):
        while not self.quit_flag:
            time.sleep(heartbeat)
            self.lock.acquire()
            if self.stop_flag:
                self.lock.release()
                continue
            try:
                self.connection.process_data_events()
            except Exception as ex:
                self.lock.release()
                raise RuntimeError("错误格式: %s" % (str(ex)))
            self.lock.release()

    def start_heartbeat(self):
        self.lock.acquire()
        if self.quit_flag:
            self.lock.release()
            return
        self.stop_flag = False
        self.lock.release()
