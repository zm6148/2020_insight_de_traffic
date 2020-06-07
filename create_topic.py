from kafka.admin import KafkaAdminClient, NewTopic
import server_name 

servers = server_name.servers

admin_client = KafkaAdminClient(bootstrap_servers=servers, client_id='test')

topic_list = []

topic_list.append(NewTopic(name="numtest", num_partitions=1, replication_factor=1))

admin_client.create_topics(new_topics=topic_list, validate_only=False)
