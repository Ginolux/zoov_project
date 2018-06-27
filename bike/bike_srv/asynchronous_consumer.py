#!/usr/bin/env python

import pika
from flask_mongoengine import mongoengine
from models import Movie


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='bikeEvents',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    mongoengine.connect(db= 'zoov', host= 'localhost', port= 27017, username= 'test', password= 'test')
    movie = Movie(name = body)
    movie.save()

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()