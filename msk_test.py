
from time import sleep
from json import dumps
from kafka import KafkaProducer


servers = ['b-1.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092',
	   'b-2.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092',
           'b-3.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092']

producer = KafkaProducer(bootstrap_servers=servers,
			value_serializer=lambda x:dumps(x).encode('utf-8'))

print(producer.bootstrap_connected())

for e in range(1000):
    data = {'number' : e}
    print(data)
    producer.send('numtest', value=data)
    print('sent')
    sleep(5)
