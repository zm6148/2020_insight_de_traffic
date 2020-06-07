from kafka.admin import KafkaAdminClient, NewTopic


servers = ['b-1.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092',
           'b-2.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092',
           'b-3.traffickafka.sn43u9.c7.kafka.us-east-1.amazonaws.com:9092']


admin_client = KafkaAdminClient(bootstrap_servers=servers, client_id='test')

topic_list = []

topic_list.append(NewTopic(name="numtest", num_partitions=1, replication_factor=1))

admin_client.create_topics(new_topics=topic_list, validate_only=False)
