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


# all cam topics
#all_cams = ['cam_1','cam_2','cam_3','cam_4','cam_5','cam_6','cam_7','cam_8','cam_9',
#            'cam_10','cam_11','cam_12','cam_14','cam_15','cam_16']

all_cams = ['cam_1','cam_2','cam_3','cam_4','cam_5','cam_6','cam_7','cam_8','cam_9',
            'cam_10','cam_11','cam_12','cam_13','cam_14','cam_15','cam_16','cam_17',
            'cam_18','cam_19','cam_20','cam_21','cam_22','cam_23','cam_24','cam_25',
            'cam_26','cam_27','cam_28'];

# make server consumers
servers = server_name.servers
consumers = []
for item in all_cams:
    consumer = KafkaConsumer(bootstrap_servers=servers,
                        auto_offset_reset='latest',
                        enable_auto_commit=True,
                        group_id=item,
                        value_deserializer=lambda x: loads(x.decode('utf-8')))
    consumer.subscribe(item)
    consumers.append(consumer)
print('created consumers')

# create app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
print('initiated app')

# setmapbox style
# current script path
scripty_path = os.path.dirname(os.path.realpath(__file__))
mapbox_access_token = 'pk.eyJ1IjoibXo4NiIsImEiOiJja2I5bWozeGgwZTJ0MnJwZjdtbHBjZjNxIn0.pSTk6D13HreCcxth26axeg'
px.set_mapbox_access_token(mapbox_access_token)
print('set map box')

# sql connection
engine = create_engine(sql_key.key, echo=False)
print('set sql engine')

app.layout = html.Div(
    html.Div([
        html.H4('Traffic Live Update'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


print('begin callbacks')
# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    
    # build data frame for mapplot
    data = []
    # read latest record from each consumer
    for consumer in consumers:
        #dummy poll
        consumer.poll()
        # go to end of the stream
        consumer.seek_to_end()
        for message in consumer:
            value = message.value
            data.append(value)
            if len(data) > 0:
               break

    # build df for ploting
    df = pd.DataFrame(data)

    # log which cams are missing
    #got_cams = df['cam_ID'].tolist()
    #missed_cams = list(set(all_cams) - set(got_cams))
    #missed_cams_sr = ' '.join([str(elem) for elem in missed_cams]) 
    df.insert(1, 'missed_cams', ' ', True)

    # save to database
    df.to_sql(name='traffic_cams', con=engine, if_exists = 'append', index=False)
    
    # start plot
    print(len(data))
    print('ploting')
    # Create the graph with subplots
    figure = px.scatter_mapbox(df, 
                               lat='lat', 
                               lon='lon', 
                               color='vehicles', 
                               size='vehicles',
                               color_continuous_scale=px.colors.sequential.thermal, 
                               size_max=15, 
                               zoom=11)
    
    figure.update_layout(uirevision = True,
                         mapbox = {'center': {'lon': -73.884704, 'lat': 40.825355}}) 
    return figure


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
