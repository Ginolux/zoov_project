from kombu import Connection, Exchange, Producer, Queue

rabbit_url = 'amqp://localhost:5672/'
conn = Connection(rabbit_url)
channel = conn.channel()
exchange = Exchange('example-exchange', type='direct')
producer = Producer(exchange=exchange, channel=channel, routing_key='BOB')
queue = Queue(name='example-queue', exchange=exchange, routing_key='BOB')
queue.maybe_bind(conn)
queue.declare()


# body = {
#         # "id": "bb2cdchl52n4orsopmtg",
#         "status": 1,
#         "location": {
#             "type": "Point",
#             "coordinates": [2.2861460, 48.8268020],
#             }
#      }


body = {
        # "id": "5b3283d4ce31602b54d169d3",
        "status": 1,
        "bike_id": "5b3283d2ce31602b54d169d2",
        "locations": [
            {
            "type": "Point",
            "coordinates": [2.2861460, 48.8268020],
            }
        ],
        "started_at": "2018-04-04T14:40:05+02:00",
        "ended_at": "2018-04-04T14:50:05+02:00"
}


producer.publish(body, serializer='json')
