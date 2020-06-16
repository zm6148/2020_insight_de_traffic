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
import cam_info

# create app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# setmapbox style
# current script path
scripty_path = os.path.dirname(os.path.realpath(__file__))
mapbox_access_token = 'pk.eyJ1IjoibXo4NiIsImEiOiJja2I5bWozeGgwZTJ0MnJwZjdtbHBjZjNxIn0.pSTk6D13HreCcxth26axeg'
px.set_mapbox_access_token(mapbox_access_token)

# sql connection
engine = create_engine(sql_key.key, echo=False)

app.layout = html.Div([
    html.Div([
        html.H4('Traffic Live Update'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0)]),
    
    html.Div([html.H4('Traffic Historical Data'),
             dcc.Dropdown(
                 id='xaxis-column',
                 options=[{'label': i, 'value': i} for i in ['Hour','Day','Week']],
                 placeholder="Select a time period"),
             dcc.Graph(id='indicator-graphic'),

             # trace plot
             dcc.Dropdown(
                 id='cam_name',
                 options=[{'label': i, 'value': j} for i, j in zip(cam_info.addresses, cam_info.cam_IDs)],
                 multi = True,
                 placeholder="Select camera location"),
             dcc.Dropdown(
                 id='time',
                 options=[{'label': i, 'value': i} for i in ['Hour','Day','Week']]),
             dcc.Graph(id='trace-graph')]) 
])

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    
    # build data frame for mapplot
    #df = pd.read_sql('SELECT * FROM traffic_cams WHERE ( unix_timestamp( ) - unix_timestamp( time ) ) < 15 GROUP BY cam_ID HAVING COUNT(*) = 1;', con=engine)

    df = pd.read_sql('SELECT time, cam_ID, lat, lon, cars, trucks, AVG(vehicles) as average_vehicles FROM traffic_cams WHERE ( unix_timestamp( ) - unix_timestamp( time ) ) < 10 GROUP BY CONCAT(cam_ID, time) HAVING COUNT(*) = 1', con=engine)

    #if len(df) < 10:
    #    df = pd.read_sql('SELECT * FROM traffic_cams WHERE ( unix_timestamp( ) - unix_timestamp( time ) ) < 60 GROUP BY cam_ID HAVING COUNT(*) = 1;', con=engine)
    # start plot
    #print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(df)
    print('ploting')
    # Create the graph with subplots
    figure = px.scatter_mapbox(df, 
                               lat='lat', 
                               lon='lon', 
                               color='average_vehicles', 
                               size='average_vehicles',
                               hover_data = ['cars', 'trucks'],
                               color_continuous_scale=px.colors.sequential.Oranges, 
                               size_max=16,
                               zoom=9)
    
    figure.update_layout(uirevision = True,
                         mapbox = {'center': {'lon':-73.862614, 'lat': 40.799312}}) 
    return figure

#def historical data plots
@app.callback(Output('indicator-graphic', 'figure'),
              [Input('xaxis-column', 'value')])         
def update_graph(xaxis_column_name):
    
    if xaxis_column_name == 'Hour':
        query ='SELECT time, cam_ID, lat, lon, AVG(vehicles) as average_vehicles FROM traffic_cams WHERE time >= NOW() - INTERVAL 1 HOUR and mod(minute(time),5) = 0 GROUP BY CONCAT(cam_ID, time)'
    if xaxis_column_name =='Day':
        query = 'SELECT time, cam_ID, lat, lon, AVG(vehicles) as average_vehicles FROM traffic_cams WHERE time >= NOW() - INTERVAL 24 HOUR and mod(minute(time),120) = 0 GROUP BY CONCAT(cam_ID, time)' 
    if xaxis_column_name =='Week':
        query = 'SELECT time, cam_ID, lat, lon, AVG(vehicles) as average_vehicles FROM traffic_cams WHERE time >= NOW() - INTERVAL 168 HOUR and mod(minute(time),840) = 0 GROUP BY CONCAT(cam_ID, time)'
    df2 = pd.read_sql(query, con=engine)
    df2['time_by_m'] = df2['time'].dt.floor('1Min') 
    df2 = df2.drop_duplicates(['time_by_m', 'cam_ID'])
    #df['time_by_m'] = df['time_by_m'] - timedelta(hours=4)
    df2['time_mark'] = df2['time_by_m'].astype(str)
    df2.sort_values(by='time')
    
    figure = px.scatter_mapbox(df2, 
                               lat='lat', 
                               lon='lon', 
                               color='average_vehicles', 
                               size='average_vehicles',
                               color_continuous_scale=px.colors.sequential.Oranges, 
                               size_max=16,
                               animation_frame= 'time_mark', 
                               animation_group = 'cam_ID',
                               zoom=9)
    return figure


# historical trace call back            
@app.callback(dash.dependencies.Output("trace-graph", 'figure'),
             [dash.dependencies.Input("cam_name", "value"),
              dash.dependencies.Input("time", "value")])
def update_trace(value_cam_ID, value_time):
    if value_time == 'Hour':
        query = 'SELECT time, cam_name, cam_ID, AVG(vehicles) as average_vehicles FROM traffic_cams WHERE time >= NOW() - INTERVAL 1 HOUR and mod(minute(time),5) = 0 GROUP BY CONCAT(cam_ID, time)'
    if value_time =='Day':
        query = 'SELECT time, cam_name, cam_ID, AVG(vehicles) as average_vehicles FROM traffic_cams WHERE time >= NOW() - INTERVAL 24 HOUR and mod(minute(time),120) = 0 GROUP BY CONCAT(cam_ID, time)'     
    if value_time =='Week':
        query = 'SELECT time, cam_name, cam_ID, AVG(vehicles) as average_vehicles FROM traffic_cams WHERE time >= NOW() - INTERVAL 168 HOUR and mod(minute(time),840) = 0 GROUP BY CONCAT(cam_ID, time)'    
    df = pd.read_sql(query, con=engine)
    df['time_by_m'] = df['time'].dt.floor('1Min') 
    df = df.drop_duplicates(['time_by_m', 'cam_ID'])
    df['time_mark'] = df['time_by_m'].astype(str)
    df.sort_values(by='time')
    
    df2 = df.loc[df['cam_ID'].isin(value_cam_ID)]
 
    figure = px.line(df2, 
                    x='time_mark', 
                    y="average_vehicles", 
                    color="cam_name",
                    line_shape = 'spline')
                    
    return figure



if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
