from kombu import Connection, Exchange, Producer, Queue


class EventsPublisher():
    def __init__(self):
        self.rabbit_url = 'amqp://localhost:5672/'
        self.conn = Connection(self.rabbit_url)
        self.channel = self.conn.channel()
        self.exchange = Exchange('gateway-exchange', type='fanout')
        self.producer = Producer(exchange=self.exchange, channel=self.channel, routing_key='gateway')
        self.queue = Queue(name='gateway-queue', exchange=self.exchange, routing_key='gateway')
        self.queue.maybe_bind(self.conn)
        self.queue.declare()

    def publish(self):
        body = {
                "id": "5b3419f51cfd8f4cfe158357",
                "status": 1,
                "location": {
                    "type": "Point",
                    "coordinates": [87.2861460, 34.4535543],
                    }
             }

        self.producer.publish(body, serializer='json')



event = EventsPublisher()
event.publish()

