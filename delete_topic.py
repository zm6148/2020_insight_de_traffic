from kafka.admin import KafkaAdminClient, NewTopic
import server_name 

servers = server_name.servers

admin_client = KafkaAdminClient(bootstrap_servers=servers, client_id='test')

topic_list = ['numtest']

admin_client.delete_topics(topics=topic_list)

