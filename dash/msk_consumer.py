from kafka import KafkaConsumer
from json import loads
import server_name 

servers = server_name.servers

consumer = KafkaConsumer('numtest',
     			bootstrap_servers=servers,
     			auto_offset_reset='earliest',
    			enable_auto_commit=True,
     			group_id='my-group',
     			value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    value = message.value
    print('recived')
    print(value['data'])
