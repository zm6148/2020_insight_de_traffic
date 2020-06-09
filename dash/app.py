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

# config kafka connection
servers = server_name.servers

consumer = KafkaConsumer(bootstrap_servers=servers,
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='my-group',
                        value_deserializer=lambda x: loads(x.decode('utf-8')))

# subscribe to topics
consumer.subscribe(['cam_1','cam_2','cam_3','cam_4','cam_5','cam_6','cam_7','cam_8','cam_9','cam_10','cam_11','cam_12'])

# create app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# setmapbox style
# current script path
scripty_path = os.path.dirname(os.path.realpath(__file__))
mapbox_access_token = 'pk.eyJ1IjoibXo4NiIsImEiOiJja2I1a3U4Y2gxNjYxMnJwN3ZvOHpkMTE0In0.T-ST6vxGWgmIJqXdIp4cGg'
px.set_mapbox_access_token(mapbox_access_token)


app.layout = html.Div(
    html.Div([
        html.H4('Traffic Live Update'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=3*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])

def update_graph_live(n):
    
    # build data frame for mapplot
    data = []
    
    #dummy poll
    consumer.poll()
    # go to end of the stream
    consumer.seek_to_end()
   
    # build df for plot
    for message in consumer:
        value = message.value
        data.append(value)
       # print(ii)
       # print('recived')
       # print(value)
       # print(len(data))
        if len(data) == 12:
            break
    
    if len(data) < 2:
        df = pd.DataFrame(data, index=[0])
    else:
        df = pd.DataFrame(data)
    
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
                         mapbox = {'center': {'lon': -73.882781, 'lat': 40.828449}}) 



    return figure


if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')
