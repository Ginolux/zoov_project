import logging
import socket
import threading

from kombu import Connection, Consumer, Exchange, Queue

from .models import Trip_db


logging.basicConfig(level=logging.DEBUG)

class EventsConsumer(threading.Thread):
    '''
    Consumer Events Processing
    '''

    def __init__(self):
        threading.Thread.__init__(self)
        self.rabbit_url = "amqp://localhost:5672/"
        self.conn = Connection(self.rabbit_url, heartbeat=10)
        self.channel = self.conn.channel()
        self.exchange = Exchange(name="gateway-exchange", type="fanout")
        self.queue = Queue(name="gateway-queue", exchange=self.exchange, routing_key="gateway")


    def process_message(self, body, message):
        '''
        Append the new location to the trip loactions if the trip status is 0 (ie bike in use)
        '''

        logging.info('*** Event received is: {}'.format(body))

        if Trip_db.objects(status='0').filter(bike_id=body['id']):
  
            trip = Trip_db.objects(status='0').get(bike_id=body['id'])
            trip.update(add_to_set__locations=body['location'])     # Append to the trip location
            trip.save()
            logging.info('*** New trip location appended')
        message.ack()


    def consume(self):
        new_conn = self.establish_connection()
        while True:
            try:
                new_conn.drain_events(timeout=2)
            except socket.timeout:
                new_conn.heartbeat_check()


    def establish_connection(self):
        consumer = Consumer(self.conn, queues=self.queue, callbacks=[self.process_message], accept=["application/json"])
        consumer.consume()

        revived_connection = self.conn.clone()
        revived_connection.ensure_connection(max_retries=3)
        channel = revived_connection.channel()
        consumer.revive(channel)
        consumer.consume()
        return revived_connection
    

    def consumer_deamon(self):
        while True:
            try:
                self.consume()
            except self.conn.connection_errors:
                logging.warning('*** Connection revived')
