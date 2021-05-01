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
px.set_mapbox_access_token(os.environ.get('MAPBOX_TOKEN'))      # If you use plotly.expres I can set the token simply like this          

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
                html.Div(id='hotel_info')
        ], className='col-md-2 m-2'),

        # Map
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': True, 'scrollZoom': True},
                style={'height':'700px','width':'1200px'}
            )
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
    # Filter the dataframe based on the selected city
    df_sub = df[df['city']==chosen_city]

    # Get the Lat and Lon for the selected city
    splittedLatLong = df_sub['latLong'].unique()[0].split(';')  
    latZoom = float(splittedLatLong[0])
    lngZoom = float(splittedLatLong[1])

    distinctDf = df.drop_duplicates(subset=['lat'])
    # lat = df['lat'].unique()
    # lng = df['lng'].unique()

    # https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html 
    # https://plotly.com/python-api-reference/generated/plotly.graph_objects.Scattermapbox.html
    # https://plotly.com/python/reference/scattermapbox/
    # https://plotly.com/python/scattermapbox/
    # Create figure
    figure = go.Figure(go.Scattermapbox(
        lat = distinctDf['lat'],
        lon = distinctDf['lng'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=10),
        # marker=go.scattermapbox.Marker(
        #     size=17,
        #     color='rgb(255, 0, 0)',
        #     opacity=0.7
        # ),
        # marker={'symbol' : 'star', 'size':16, 'allowoverlap':True},
        unselected={'marker' : {'opacity':1}},
        selected={'marker' : {'opacity':0.5, 'size':25}},
        hoverinfo='lon+lat+text',                                   # Examples: "lon", "lat", "lon+lat", "lon+lat+text", "all", 'none', 'skip'
        hovertext=distinctDf['Hotel_Name'],
        # customdata=df_sub
    ))

    # locations[0].update_traces(marker_colorbar_outlinecolor='black',marker_colorbar_outlinewidth=2)    
    figure.update_layout(
        uirevision= 'foo', #preserves state of figure/map after callback activated
        clickmode= 'event+select',
        # autosize=True,
        hovermode='closest',
        hoverdistance=2,
        title=dict(text="Hotel Reviews Europe?",font=dict(size=50, color='green')),
        mapbox=dict(
            accesstoken=os.environ.get('MAPBOX_TOKEN'),
            # bearing=0,
            style='outdoors',  # other option might be 'dark', light, basic, satellite etc. - for more https://plotly.com/python/scattermapbox/
            center={'lat':latZoom,'lon':lngZoom},
            # pitch=0,     # This make the map little bit tilted
            zoom=14
        ),
    )

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
# # callback for ...
@app.callback(
    Output('hotel_info', 'children'),
    [Input('graph', 'clickData')])
def display_click_data(clickData):
    if clickData is None:
        return 'Click on any bubble'
    else:
        print (clickData)
        lat=clickData['points'][0]['lat']
        lng=clickData['points'][0]['lon']

        selectedHotelInfo = df[(df['lat']==lat) & (df['lng']==lng)]

        if selectedHotelInfo is None:
            return 'No Data'
        else:
            # return html.A(clickData, href=clickData, target="_blank")
            print(selectedHotelInfo.head(4))
            return selectedHotelInfo.Hotel_Name.unique()
# #--------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)