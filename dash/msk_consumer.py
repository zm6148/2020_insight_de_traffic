from kafka import KafkaConsumer
from json import loads
import server_name 

servers = server_name.servers

consumer = KafkaConsumer('cam_1',
     			bootstrap_servers=servers,
     			auto_offset_reset='earliest',
    			enable_auto_commit=True,
     			group_id='my-group',
     			value_deserializer=lambda x: loads(x.decode('utf-8')))

#dummy poll
consumer.poll()
#go to end of the stream
consumer.seek_to_end()

ii = 0
for message in consumer:
    ii = ii + 1
    print(ii)
    value = message.value
    print('recived')
    print(value)
