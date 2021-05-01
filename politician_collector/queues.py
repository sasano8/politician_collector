from asy_rabbitmq import Rabbitmq
from . import config

host = config.RabbitmqConfig().RABBITMQ_HOST
rabbitmq = Rabbitmq(host=host)
queue_default = rabbitmq.consumer(queue_name="default", auto_ack=False)
queue_extract = rabbitmq.consumer(queue_name="extract", auto_ack=True)
queue_transform = rabbitmq.consumer(queue_name="transform", auto_ack=True)
