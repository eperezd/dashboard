# coronavirus dashboard
# Ing. Ms. E.R.P.D

# 0. setup
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# 1. Get Data. traemos la data desde una web que presenta info todos los dias
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

# 2. formates templates

external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
tickFont={'size':8, 'color':"rgb(30,30,30)"}

# 3. funcion get Data



def loadData(filename):
    data= pd.read_csv(url+filename)
    return data

# 4. read data and format the data
data = loadData("time_series_covid19_confirmed_global.csv")
data= data.drop(['Lat', 'Long','Province/State'], axis=1)
data=data.melt(id_vars=['Country/Region'], var_name= 'date',value_name="Confirmed")
data=data.astype({'date':'datetime64[ns]',"Confirmed":'Int64'}, errors= 'ignore')
data['dateStr']=data['date'].dt.strftime('%b %d,%Y')

# 5. prepare a list of countries

countries=data['Country/Region'].unique()
countries.sort()
options=[{'label':c, 'value':c}for c in countries]

#6. Dashboard Layout

app =dash.Dash()
app.title='Coronavirus Dashboard'

app.layout = html.Div([
    # Header
    html.H1('Covid 19 Casos confrimados'),
    #Dropdown
    html.Div(dcc.Dropdown(id= 'country-picker', options = options, value= 'Peru'),
    style={'width':'25%'}),
    #plot
    dcc.Graph(
        id='confirmed-cases',
        config={'displayModebar':False}
    )


])  # end layout

# add callback  to support the interactive componentes

@app.callback(Output(component_id='confirmed-cases', component_property='figure'),
               [Input(component_id='country-picker', component_property='value')])

def update_bar_chart(selected_country):
    filtered_df=data[data['Country/Region']== selected_country]
    fig = go.Figure(data=[
          go.Bar(name='Confirmados', x=filtered_df['dateStr'],y=filtered_df['Confirmed'],marker_color='firebrick')
    ])
    fig.update_layout(
        title='Casos confirmados para {}'.format(selected_country), 
        xaxis=dict(tickangle= -90, ticktext= data.dateStr, tickfont= tickFont, type='category')
    )
    return fig


app.run_server()