import pandas as pd
import numpy as np
import dash                     #(version 1.0.0)
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go
import plotly.express as px

import os
px.set_mapbox_access_token(os.environ.get('MAPBOX_TOKEN'))

script_dir = os.path.dirname(__file__)                          # Script directory
full_path = os.path.join(script_dir, '../Hotel.csv')    # Full Directory to the CSV
df = pd.read_csv(full_path)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.Div([

        # Side Navbar
        html.Div([
            html.Label(['Choose City:'],style={'font-weight': 'bold', "text-align": "center"}),
             dcc.Dropdown(
                    id='hotelCity',
                    options=
                    [{'label': city, 'value': city} for city in df['city'].unique()],
                    value='Amsterdam',
                    # multi=True,
                    className='text-dark'
                ),
                html.P(id='hotel_info')
        ], className='col-md-2 m-2'),

        # Map
        html.Div([
            dcc.Graph(id='graph')
        ], className='col-md-8'
        ),

    ], className='row'
    ),

], className=''
)

# Output of Graph
@app.callback(Output('graph', 'figure'),
              [Input('hotelCity', 'value'),]
              )
def update_figure(chosen_city):
    df_sub = df[df['city']==chosen_city]

    df_sub['latLong'].head()

    splittedLatLong = df_sub['latLong'].unique()[0].split(';')  
    latZoom = float(splittedLatLong[0])
    lngZoom = float(splittedLatLong[1])

    distinctDf = df.drop_duplicates(subset=['lat'])

    # lat = df['lat'].unique()
    # lng = df['lng'].unique()

    # https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
    # https://plotly.com/python/scattermapbox/
    # Create figure

        # Create figure
    locations=[go.Scattermapbox(
                    lat = distinctDf['lat'],
                    lon = distinctDf['lng'],
                    mode='markers',
                    # marker={'symbol' : 'star', 'size':16, 'allowoverlap':True},
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':25}},
                    hoverinfo='lon+lat+text',                                   # Examples: "lon", "lat", "lon+lat", "lon+lat+text", "all", 'none', 'skip'
                    hovertext=distinctDf['Hotel_Name'],
                    # customdata=df_sub['website']
    )]

    # locations[0].update_traces(marker_colorbar_outlinecolor='black',marker_colorbar_outlinewidth=2)    
    figure = {
            'data': locations,
            'layout': go.Layout(
                uirevision= 'foo', #preserves state of figure/map after callback activated
                clickmode= 'event+select',
                hovermode='closest',
                hoverdistance=2,
                title=dict(text="Where to Recycle My Stuff?",font=dict(size=50, color='green')),
                mapbox=dict(
                    accesstoken=os.environ.get('MAPBOX_TOKEN'),
                    bearing=50,
                    style='light',  # other option might be 'dark'
                    center=dict(
                        lat=latZoom,
                        lon=-lngZoom
                    ),
                    # pitch=40,     # This make the map little bit tilted
                    zoom=6
                ),
            )
        }

    return figure




    # fig = px.scatter_mapbox(
    #                         distinctDf,
    #                         lat='lat', 
    #                         lon='lng',     
    #                         # color="peak_hour", 
    #                         # size="car_hours",
    #                         color_continuous_scale=px.colors.cyclical.IceFire, 
    #                         size_max=15, 
    #                         zoom=15,
    #                         hover_name = 'Hotel_Name',
    #                         width=1600,
    #                         height=800,
    #                         center={'lat':latZoom,'lon':lngZoom})
    # return fig

#---------------------------------------------------------------
# callback for Web_link
@app.callback(
    Output('hotel_info', 'children'),
    [Input('graph', 'clickData')])
def display_click_data(clickData):
    if clickData is None:
        return 'Click on any bubble'
    else:
        print (clickData)
        the_link=clickData
        if the_link is None:
            return 'No Data'
        else:
            # return html.A(clickData, href=clickData, target="_blank")
            return the_link['points'][0]['hovertext']
# #--------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)