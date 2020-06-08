import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from dash.dependencies import Input, Output
import plotly_express as px
import pandas as pd 

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
            interval=1*1000, # in milliseconds
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
    # Collect some data
    # df = px.data.carshare()
    data1 = {'cars': 11, 
            'trucks': 1, 
            'person': 0, 
            'bicycle': 0, 
            'motorcycle': 0, 
            'bus': 0, 
            'vehicles': 12, 
            'cam_ID': 'cam_1', 
            'cam_name': 'I-95 Weeks Avenue', 
            'lat': 40.8452, 
            'lon': -73.907545, 
            'facing': 'south', 
            'time': '2020-06-08 04:18:28', 
            'region': 500}
    
    data2 = {'cars': 11, 
            'trucks': 1, 
            'person': 0, 
            'bicycle': 0, 
            'motorcycle': 0, 
            'bus': 0, 
            'vehicles': 34, 
            'cam_ID': 'cam_1', 
            'cam_name': 'I-278 at Whittier Street', 
            'lat': 40.822477, 
            'lon': -73.885890, 
            'facing': 'south', 
            'time': '2020-06-08 04:18:28', 
            'region': 550}
            
    data.append(data1)
    data.append(data2)
            
    if len(data) < 2:
        df = pd.DataFrame(data, index=[0])
    else:
        df = pd.DataFrame(data)

    # Create the graph with subplots
    figure = px.scatter_mapbox(df, 
                               lat='lat', 
                               lon='lon', 
                               color='vehicles', 
                               size='region',
                               color_continuous_scale=px.colors.sequential.Inferno_r, 
                               size_max=15, zoom=11.5)

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
