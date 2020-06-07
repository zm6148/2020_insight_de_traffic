
from time import sleep
from json import dumps
from kafka import KafkaProducer
import server_name 

servers = server_name.servers

producer = KafkaProducer(bootstrap_servers=servers,
			value_serializer=lambda x:dumps(x).encode('utf-8'))

print(producer.bootstrap_connected())

for e in range(1000):
    data = {'number' : e}
    print(data)
    producer.send('numtest', value=data)
    print('sent')
    sleep(5)
