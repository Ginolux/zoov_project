import logging

from kombu import Connection, Exchange, Producer, Queue


logging.basicConfig(level=logging.DEBUG)

class EventsPublisher():
    def __init__(self):
        self.rabbit_url = 'amqp://localhost:5672/'
        self.conn = Connection(self.rabbit_url)
        self.channel = self.conn.channel()
        self.exchange = Exchange(name='gateway-exchange', type='fanout')
        self.producer = Producer(exchange=self.exchange, channel=self.channel, routing_key='gateway')
        self.queue = Queue(name='gateway-queue', exchange=self.exchange, routing_key='gateway')
        self.queue.maybe_bind(self.conn)
        self.queue.declare()

    def publish(self, body):
        # body = {
        #         # "id": "bb2cdchl52n4orsopmtg",
        #         "status": 1,
        #         "location": {
        #             "type": "Point",
        #             "coordinates": [2.2861460, 48.8268020],
        #             }
        #      }

        self.producer.publish(body, serializer='json')
        logging.info('*** Event published is: {}'.format(body))

