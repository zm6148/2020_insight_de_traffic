from kafka import KafkaConsumer
from json import loads

servers = ['b-1.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092',
           'b-2.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092',
           'b-3.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092']


consumer = KafkaConsumer('numtest',
     			bootstrap_servers=servers,
     			auto_offset_reset='earliest',
    			enable_auto_commit=True,
     			group_id='my-group',
     			value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    value = message.value
    print('recived')
    print(value)
