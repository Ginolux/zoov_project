import pika, os

url = os.environ.get('RABBITMQ_URL', 'amqp://localhost')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to the RabbitMQ
channel = connection.channel() # Start a channel
channel.queue_declare(queue='bikeprocess') # Declare a queue

# Send a message
message = "{'bikes': 'we have lots of informations about bikes'}"

channel.basic_publish(exchange='', routing_key='bikeprocess', body=message)
print('[x] Message sent to consumer')
connection.close()

