from kafka import KafkaConsumer
from json import loads
import server_name 

servers = server_name.servers

consumer = KafkaConsumer(bootstrap_servers=servers,
     			auto_offset_reset='earliest',
    			enable_auto_commit=True,
     			#group_id='my-group',
                        group_id='cams',
     			value_deserializer=lambda x: loads(x.decode('utf-8')))

consumer.subscribe(['cam_1'])

#dummy poll
consumer.poll()

#go to end of the stream
consumer.seek_to_end()

data = consumer.poll(1000)

print(data)

for tp, message in data.items():
        # print(tp)
        print(message)
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print (message[1].value)

#ii = 0
#for message in consumer:
#    ii = ii + 1
#    print(ii)
#    value = message.value
#    print('recived')
#    print(value)
