from confluent_kafka import Producer

# Change to point to your kafka installation
p = Producer({'bootstrap.servers': 'b-1.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092,b-3.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092,b-2.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092'})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

for e in range(0, 100):
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)
    data = {'num': e}
    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    p.produce('mytopic', data, callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()
