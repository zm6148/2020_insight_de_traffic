from kafka.admin import KafkaAdminClient, NewTopic
import server_name 

servers = server_name.servers

admin_client = KafkaAdminClient(bootstrap_servers=servers, client_id='test')

# all cam topics
all_cams = ['cam_1','cam_2','cam_3','cam_4','cam_5','cam_6','cam_7','cam_8','cam_9','cam_10','cam_11','cam_12','cam_14','cam_15','cam_16']
topic_list = all_cams

admin_client.delete_topics(topics=topic_list)

