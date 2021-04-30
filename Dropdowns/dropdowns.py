import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os

app = dash.Dash(__name__)

#---------------------------------------------------------------
script_dir = os.path.dirname(__file__)                          # Script directory
full_path = os.path.join(script_dir, '../Hotel_Reviews.csv')    # Full Directory to the CSV
hotelDf = pd.read_csv(full_path)                                # Read csv to Dataframe

#---------------------------------------------------------------
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='your_graph')
    ],className=''),
    html.P( id='total',className='text-center'),

    html.Div([
        html.Label(['Choose column:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='my_dropdown',
            options=[
                {'label': 'Positive', 'value': '1'},
                {'label': 'Negative', 'value': '0'},
            ],
            optionHeight=35,                    #height/space between dropdown options
            value='1',                          #dropdown value selected automatically when page loads
            disabled=False,                     #disable dropdown value selection
            multi=False,                        #allow multiple dropdown values to be selected
            searchable=True,                    #allow user-searching of dropdown values
            search_value='',                    #remembers the value searched in dropdown
            placeholder='Please select...',     #gray, default text shown when no option is selected
            clearable=True,                     #allow user to removes the selected value
            style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
            # className='select_box',           #activate separate CSS document in assets folder
            # persistence=True,                 #remembers dropdown value. Used with persistence_type
            # persistence_type='memory'         #remembers dropdown value selected until...
            ),                                  #'memory': browser tab is refreshed
                                                #'session': browser tab is closed
                                                #'local': browser cookies are deleted
    ],className='three columns'),

])

#---------------------------------------------------------------
# Connecting the Dropdown values to the graph
@app.callback(
    [Output(component_id='your_graph', component_property='figure'),Output(component_id='total', component_property='children')],
    [Input(component_id='my_dropdown', component_property='value')]
)
def build_graph(column_chosen):

    # Select Positive Review or Negative review based on the selection of the user
    if column_chosen == '1':
        dff=hotelDf[hotelDf['Reviewer_Score'] > 5.5]
    elif column_chosen == '0':
        dff=hotelDf[hotelDf['Reviewer_Score'] < 5.5]

    # Get only the column with countries with a total more then 500 reviews
    dff2 = dff.Reviewer_Nationality.value_counts().loc[lambda x: x>500].reset_index()
    dff3 = dff2.rename(columns = {'index':'country'})

    # Create Pie Figure
    fig = px.pie(
        dff3,
        names='country', 
        values='Reviewer_Nationality', 
        color='country',
        # title='Postive or Negative reviews and Countries', 
        width = 1200,                                           
        height = 700,
        # hole=0.5,
        labels={'Reviewer_Nationality':'AmountOfReviews'},      # Custome label view when hoveredd  
        hover_name='country',                                   # The value that should be bold when hovered
        # hover_data=[''],                                      # Extra column that you want to add to the hover data 
        template='presentation',                                # There are many different templates
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title={'text':'Postive or Negative reviews and Countries',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})

    infoText = 'Total Number of '+ ('postive ' if column_chosen=='1' else 'negative ')+ 'reviews: ' +str(dff3['Reviewer_Nationality'].sum())
    return fig, infoText

if __name__ == '__main__':
    app.run_server(debug=True)