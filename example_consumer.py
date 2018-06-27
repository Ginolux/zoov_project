import pika, os, time

def bike_process_function(msg):
    print('Bike processing')
    print('[x] Received msg: {}'.format(msg))

    time.sleep(5) # delay for 5 sec
    print('Bike processing finished')


url = os.environ.get('RABBITMQ_URL', 'amqp://localhost')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to the RabbitMQ
channel = connection.channel() # Start a channel
channel.queue_declare(queue='bikeprocess') # Declare a queue


# Function which is called on incoming messages
def callback(ch, method, properties, body):
    bike_process_function(body)

# Set up subscription on the queue
channel.basic_consume(callback, queue='bikeprocess', no_ack=True)

# Start consuming (Blocks)
channel.start_consuming()
connection.close()