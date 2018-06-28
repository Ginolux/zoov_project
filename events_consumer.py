import socket
import threading

from kombu import Connection, Consumer, Exchange, Queue


class EventsConsumer():
    def __init__(self):
        self.rabbit_url = "amqp://localhost:5672/"
        self.conn = Connection(self.rabbit_url, heartbeat=10)
        self.exchange = Exchange("example-exchange", type="direct")
        self.queue = Queue(name="example-queue", exchange=self.exchange, routing_key="BOB")


    def process_message(self, body, message):
        # bike = Bike_db( 
        #             status=body['status'],
        #             location=body['location'])

        # id = body['id']
        # if Bike_test.objects.with_id(id):
        #     bike.update()
        #     bike.save()


        # bike = Bike_test( 
        #                 status=body['status'],
        #                 location=body['location'])
        # bike.update()
        # bike.save()
        # bike.drop_collection()

        print("The body is {}".format(body))
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
                print("connection revived")
