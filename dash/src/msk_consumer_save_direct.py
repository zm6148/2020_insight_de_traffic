import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from dash.dependencies import Input, Output
import plotly_express as px
import pandas as pd
from kafka import KafkaConsumer
from json import loads
import server_name 
import time
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from sqlalchemy import create_engine
import sql_key
from datetime import datetime

# config kafka connection
servers = server_name.servers

consumer = KafkaConsumer(bootstrap_servers=servers,
                        auto_offset_reset='latest',
                        enable_auto_commit=False,
                        group_id='1_consumer_all_cams',
                        value_deserializer=lambda x: loads(x.decode('utf-8')))

# subscribe to topics
all_cams = ['cam_1','cam_2','cam_3','cam_4','cam_5','cam_6','cam_7','cam_8','cam_9','cam_10','cam_11','cam_12','cam_14','cam_15','cam_16',
            'cam_13','cam_17','cam_18','cam_19','cam_20','cam_21','cam_22','cam_23','cam_24','cam_25','cam_26','cam_27','cam_28','cam_29',
            'cam_30','cam_31','cam_32','cam_33','cam_34','cam_35','cam_36','cam_37','cam_38','cam_39','cam_40','cam_41','cam_42','cam_43',
            'cam_44','cam_45','cam_46','cam_47','cam_48','cam_49','cam_50','cam_51','cam_52','cam_53','cam_54','cam_55','cam_56']

consumer.subscribe(all_cams)
print('consumer done')

# sql connection
engine = create_engine(sql_key.key, echo=False)

   
# build data frame for mapplot
data = []
#dummy poll
consumer.poll()
# go to end of the stream
consumer.seek_to_end()

# build df 
for message in consumer:
    value = message.value
    # build df for ploting
    df = pd.DataFrame(value, index=[0])

    # log missing cams 
    df.insert(1, 'missed_cams', ' ', True)
    
    # save to database
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(df)
    df.to_sql(name='traffic_cams', con=engine, if_exists = 'append', index=False)
