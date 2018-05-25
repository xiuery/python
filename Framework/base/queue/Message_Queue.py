
"""RabbitMQ消息队列"""


import pika
from copy import deepcopy
from abc import ABCMeta, abstractmethod
from pika import credentials
from base.queue.Rabbitmq_Heartbeat import RabbitMQHeartbeat


class IMessageConnection(metaclass=ABCMeta):
    # 消息连接接口类，所有消息连接类都必须实现以下接口
    @abstractmethod
    def get_connection(self):
        """
        :return: 返回连接实例
        """
        return


class IMessageCallBack(metaclass=ABCMeta):
    # 消息回调接口类，所有需要使用到消息回调的类都需要继承该类，
    # 并实现callback方法，否则无法完成消息回调

    @abstractmethod
    def callback(self):
        """
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:消息成功返回True，否则False
        """
        return


class IMessageHandler(metaclass=ABCMeta):
    # 消息处理接口类，所有消息类型类都必须实现以下接口

    @abstractmethod
    def close(self):
        # 关闭连接
        return

    @abstractmethod
    def start_consuming(self, callback):
        """开始消费消息
        :param callback:回调函数
        :return:
        """
        return


class ConnectionFactory(object):
    @staticmethod
    def get_instance(class_name, connect_params):
        """获取消息连接实例
        :param class_name:消息连接类名
        :param connect_params:连接参数
        :return:连接实例
        """
        if 'RabbitMQConnection' == class_name:
            return RabbitMQConnection(connect_params)


class RabbitMQConnection(IMessageConnection):
    def __new__(cls, connect_params):
        if not hasattr(cls, '_inst'):
            cls._inst = super(RabbitMQConnection, cls).__new__(cls)
        return cls._inst

    def __init__(self, connect_params):
        self.params = connect_params
        self.connection = None

    def get_connection(self):
        self.connection = self.connect()
        return self.connection

    @staticmethod
    def credentials(username, password):
        """返回一个plain credentials对象
        :param username:用户名
        :param password:密码
        :return:pika_credentials.PlainCredentials
        """
        return credentials.PlainCredentials(username, password)

    def connect(self):
        params = deepcopy(self.params)
        username = params.pop('username')
        password = params.pop('password')
        certificate = self.credentials(username, password)
        connect_params = pika.ConnectionParameters(credentials=certificate,
                                                   **params)
        if not self.connection:
            return pika.BlockingConnection(connect_params)


class MessageHandlerFactory(object):
    # 负责消息处理程序的创建
    @staticmethod
    def get_instance(class_name, connect_params, message_params):
        """获取消息处理实例
        :param class_name:消息处理类名
        :param connect_params:
        :param message_params:消息处理参数
        :return:class_name实例
        """
        if 'RabbitMQ' == class_name:
            return RabbitMQMessageHandler(connect_params, message_params)


class RabbitMQMessageHandler(IMessageHandler):
    # RabbitMQ消息处理程序实现
    def __init__(self, connect_params, message_params):
        '''初始化函数，需要传入消费的配置参数
        :param connect_params:消费的配置参数
        :param message_params:None
        '''
        self.params = message_params
        self.channel = None
        self.connection = ConnectionFactory.get_instance('RabbitMQConnection', connect_params).get_connection()

    def start_consuming(self, callback):
        '''启动消费，消息的类型根据初始化传入的配置参数来决定启动哪种消费模式
        :param callback:回调函数
        :return:None
        '''
        heartbeat = RabbitMQHeartbeat(self.connection)
        heartbeat.start()
        heartbeat.start_heartbeat()
        self.on_bind()
        self._consuming_queues(callback)

    def publish_message(self, data):
        """发布到交换机"""
        channel = self._get_channel()
        routing_key = self.params.get('routing_key')
        delivery_mode = self.params.get("delivery_mode")
        self.channel.basic_publish(exchange=self.params.get("exchange"),
                                   routing_key=routing_key,
                                   body=data,
                                   properties=pika.BasicProperties(
                                       delivery_mode=delivery_mode)
                                   )
        channel.close()

    def publish_message_queue(self, data):
        """发布到队列"""
        channel = self._get_channel()
        queue_name = self.params.get('task_queue')
        durable = self.params.get('durable')
        delivery_mode = self.params.get("delivery_mode")
        channel.queue_declare(queue=queue_name, durable=durable)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=data,
                              properties=pika.BasicProperties(
                                  delivery_mode=delivery_mode)
                              )
        channel.close()

    def _consuming_queues(self, callback_obj=None):
        # 竞争消费模式
        channel = self._get_channel()
        queue_name = self.params.get('task_queue')
        durable = self.params.get('durable')
        prefetch_count = self.params.get('prefetch_count')
        channel.queue_declare(queue=queue_name, durable=durable)

        def callback(ch, method, properties, body):
            if isinstance(callback_obj, IMessageCallBack):
                if callback_obj.callback(ch, method, properties, body):
                    ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=prefetch_count)
        channel.basic_consume(callback, queue=queue_name)
        channel.start_consuming()

    def setup_exchange(self):
        """声明交换机"""
        self.channel.exchange_declare(exchange=self.params.get("exchange"),
                                      exchange_type=self.params.get("exchange_type"),
                                      durable=self.params.get("durable"))

    def setup_queue(self):
        """队列申明"""
        for queue_name in self.params.get("publish_data_queue"):
            self.channel.queue_declare(queue=queue_name,
                                       durable=self.params.get("durable"))

    def on_bind(self):
        """绑定交换机与队列"""
        self._get_channel()
        self.setup_exchange()
        self.setup_queue()
        for queue_name in self.params.get("publish_data_queue"):
            self.channel.queue_bind(queue=queue_name,
                                    exchange=self.params.get("exchange"),
                                    routing_key=self.params.get("routing_key"))

    def _get_channel(self):
        """获取通道"""
        self.channel = self.connection.channel()
        return self.channel

    def close_channel(self):
        """关闭信道"""
        self.channel.close()

    def close(self):
        """关闭连接"""
        self.connection.close()
