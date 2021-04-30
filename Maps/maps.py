import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os

px.set_mapbox_access_token(os.environ.get('MAPBOX_TOKEN'))
df = px.data.carshare()
fig = px.scatter_mapbox(
                        df, 
                        lat="centroid_lat", 
                        lon="centroid_lon",     
                        color="peak_hour", 
                        size="car_hours",
                        color_continuous_scale=px.colors.cyclical.IceFire, 
                        size_max=15, 
                        zoom=15)

#---------------------------------------------------------------
# tips = px.data.tips()
script_dir = os.path.dirname(__file__)                          # Script directory
full_path = os.path.join(script_dir, '../Hotel_Reviews.csv')    # Full Directory to the CSV
hotelDf = pd.read_csv(full_path)                                # Read csv to Dataframe

#---------------------------------------------------------------

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div(
    [
        html.H1("Demo: Plotly Express in Dash with Tips Dataset"),
        dcc.Graph(figure=fig,id="graph", style={"width": "75%", "display": "inline-block"}),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)