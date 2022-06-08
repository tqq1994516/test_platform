import re
import time

import pulsar

from pulsar.schema import AvroSchema, Record, String

from settings import PULSAR_TENANTS, PULSAR_HOST, PULSAR_PORT


class UiSelectorSchema(Record):
    _avro_namespace = f'{PULSAR_TENANTS}.ui_test.ui_selector'
    request_id = String()
    method = String()
    path = String()


def pulsar_producer(topic, message: UiSelectorSchema, is_async=False, callback=None):
    client = pulsar.Client(f'pulsar://{PULSAR_HOST}:{PULSAR_PORT}')
    producer = client.create_producer(f'persistent://{PULSAR_TENANTS}/ui_test/{eval(topic.split("=")[-1])}',
                                      schema=AvroSchema(UiSelectorSchema))
    if is_async:
        producer.send_async(message, callback=callback)
    else:
        msg_id = producer.send(message)
        print(f'Message published with id: {msg_id}')
    client.close()


def pulsar_consumer():
    client = pulsar.Client(f'pulsar://{PULSAR_HOST}:{PULSAR_PORT}')
    consumer = client.subscribe(re.compile(f'persistent://{PULSAR_TENANTS}/ui_test/*'), 'web_test',
                                schema=AvroSchema(UiSelectorSchema))
    while True:
        msg = consumer.receive()
        try:
            print("Received message '{}' id='{}' value='{}'".format(msg.data(), msg.message_id(), msg.value()))
            # Acknowledge successful processing of the message
            consumer.acknowledge(msg)
        except Exception as e:
            # Message failed to be processed
            consumer.negative_acknowledge(msg)
    client.close()


# class PulsarPublisher(AbstractPublisher):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client = pulsar.Client(f'pulsar://{funboost_config.PULSAR_HOST}:{funboost_config.PULSAR_PORT}')
#
#     def concrete_realization_of_publish(self, msg: str):
#         self.producer = self.client.create_producer(self._queue_name, schema=JsonSchema(UiSelectorSchema))
#         self.producer.send(msg)
#
#     def clear(self):
#         self.logger.warning('未找到pulsar清空队列方法')
#
#     def get_message_count(self):
#         self.logger.warning('未找到pulsar获取队列消息数量方法')
#         return -1
#
#     def close(self):
#         self.client.close()
#
#
# class PulsarConsumer(AbstractConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client = pulsar.Client(f'pulsar://{funboost_config.PULSAR_HOST}:{funboost_config.PULSAR_PORT}')
#
#     def _shedual_task(self):
#         self.consumer = self.client.subscribe(self._queue_name, 'web_test', schema=JsonSchema(UiSelectorSchema))
#         while True:
#             msg = self.consumer.receive()
#             try:
#                 print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
#                 # Acknowledge successful processing of the message
#                 self.consumer.acknowledge(msg)
#             except Exception:
#                 # Message failed to be processed
#                 self.consumer.negative_acknowledge(msg)
#                 continue
#             kw = {'consumer': self.consumer, 'message': msg, 'body': json.loads(msg.value())}
#             self._submit_task(kw)
#         self.client.close()
#
#     def _confirm_consume(self, kw):
#         pass  # shedual_task 中已经调用了 acknowledge
#
#     def _requeue(self, kw):
#         pass  # shedual_task 中已经调用了 negative_acknowledge
#
#
# BROKER_KIND_PULSAR = 20
# register_custom_broker(BROKER_KIND_PULSAR, PulsarPublisher, PulsarConsumer)  # 核心，这就是将自己写的类注册到框架中，框架可以自动使用用户的类，这样用户无需修改框架的源代码了。
