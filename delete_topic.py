from kafka.admin import KafkaAdminClient, NewTopic
import server_name 

servers = server_name.servers

admin_client = KafkaAdminClient(bootstrap_servers=servers, client_id='test')

all_cams = ['cam_1',
           'cam_2',
           'cam_3',
           'cam_4',
           'cam_5',
           'cam_6',
           'cam_7',
           'cam_8',
           'cam_9',
           'cam_10',
           'cam_11',
           'cam_12',
           'cam_13',
           'cam_14',
           'cam_15',
           'cam_16',
           'cam_17',
           'cam_18',
           'cam_19',
           'cam_20',
           'cam_21',
           'cam_22',
           'cam_23',
           'cam_24',
           'cam_25',
           'cam_26',
           'cam_27',
           'cam_28',
           'cam_29',
           'cam_30',
           'cam_31',
           'cam_32',
           'cam_33',
           'cam_34',
           'cam_35',
           'cam_36',
           'cam_37',
           'cam_38',
           'cam_39',
           'cam_40',
           'cam_41',
           'cam_42',
           'cam_43',
           'cam_44',
           'cam_45',
           'cam_46',
           'cam_47',
           'cam_48',
           'cam_49',
           'cam_50',
           'cam_51',
           'cam_52',
           'cam_53',
           'cam_54',
           'cam_55',
           'cam_56']

topic_list = all_cams

admin_client.delete_topics(topics=topic_list)

