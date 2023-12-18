import pandas as pd
import dash
from dash import dcc , html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.offline as py
# pio.renderers.default = 'browser'

df1 = pd.read_csv("~/strongerbc/data/research_and_development_1.csv")
df = df1[df1['Year'] >= 2000]
app = dash.Dash(__name__)

# Labels and Steps of Year Range
labels = {str(year): str(year) for year in range(df['Year'].min(), df['Year'].max() + 1 , 5)}
steps = {str(year): '' for year in range(df['Year'].min(), df['Year'].max() + 1)}
marks = {**steps, **labels}


app.layout = html.Div([
    html.Div([
        dcc.Graph(id='value-graph')
    ], style={'width': '100%', 'display': 'inline-block'}),
    html.Div([
        dcc.RangeSlider(
            id='year-slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=[df['Year'].min(), df['Year'].max()],
            marks=marks,
            step=None
        ),
        dcc.Dropdown(
            id='geo-dropdown',
            options=[{'label': i, 'value': i} for i in df['GEO'].unique()],
            value=df['GEO'].unique()[0]
        ),
        dcc.Dropdown(
            id='Funder-dropdown',
            options=[{'label': i, 'value': i} for i in df['Funder'].unique()],
            value=df['Funder'].unique()[0]
        ),
        dcc.Dropdown(
            id='Performer-dropdown',
            options=[{'label': i, 'value': i} for i in df['Performer'].unique()],
            value=df['Performer'].unique()[0]
        ),
        dcc.Dropdown(
            id='ScienceType-dropdown',
            options=[{'label': i, 'value': i} for i in df['Science type'].unique()],
            value=df['Science type'].unique()[0]
        ),
        dcc.Dropdown(
            id='Prices-dropdown',
            options=[{'label': i, 'value': i} for i in df['Prices'].unique()],
            value=df['Prices'].unique()[0]
        )
    ], style={'width': '100%', 'display': 'inline-block'}),
])

@app.callback(
    Output('value-graph', 'figure'),
    [Input('year-slider', 'value'),
     Input('geo-dropdown', 'value'),
     Input('Funder-dropdown', 'value'),
     Input('Performer-dropdown', 'value'),
     Input('ScienceType-dropdown', 'value'),
     Input('Prices-dropdown', 'value')],
)
def update_graph(year_range, geo_value, Funder_value, Performer_value, ScienceType_value, Prices_value):
    dff = df[(df['Year'] >= year_range[0]) & 
             (df['Year'] <= year_range[1]) & 
             (df['GEO'] == geo_value)      & 
             (df['Funder'] == Funder_value)&
             (df['Performer'] == Performer_value) &
             (df['Science type'] == ScienceType_value) &
             (df['Prices'] == Prices_value)]

    fig = px.line(dff, x="Year", y="VALUE", title='Investment in Innovation', template='plotly_white')
    fig.update_traces(mode='markers+lines')
    fig.update_yaxes(title_text=f'{Prices_value} (in millions $ )')
    fig.update_layout(
    title={
        'text': "Trends in Innovation Investment",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)