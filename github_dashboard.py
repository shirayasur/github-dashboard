import dash
from dash import Dash, html, dcc, dash_table
from dash.dependencies import ClientsideFunction, Input, Output
from sqlalchemy import create_engine
import pymysql 

from gh_dash_functions import *

from config import DB_CONNECTION_STRING


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
sqlEngine = create_engine(DB_CONNECTION_STRING, pool_recycle=3600)

def get_dbConnection():
    dbConnection = sqlEngine.connect()
    return dbConnection

pd.options.mode.chained_assignment = None

#generate Repo Growth graph for dropdown        
def generate_graph(repo_name):
    dbc = get_dbConnection()
    repo_df = repo_create_df(dbc)
    g_df = github_growth(repo_df,repo_name)
    g_graph = growth_graph(g_df)
    return g_graph

def generate_dropdown():
    dbc = get_dbConnection()
    return get_dropdown_names(dbc)

#Dashboard
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


server = app.server

app.layout = html.Div([
    
    dcc.Interval(
            id='interval-component',
            interval=1*1000*60*60*12, # in milliseconds
            n_intervals=0
        ),  
    
    html.H1(children='GitHub Repositories Comparison'),
    
    
    dcc.Tabs([
        
    dcc.Tab(label='Repo Stars and Watchers Comparison', children=[
        dcc.Graph(id = 'stars_watchers_graph'),
    
    dcc.Markdown('Information from GitHub API is used to show the amount of stars in yellow and watchers in green.')
    
    ]),
        
    dcc.Tab(label='Repo Stars Growth Comparison', children=[
        dcc.Graph(id = 'stars_growth_graph'),
    
    dcc.Markdown('Information from GitHub API is used to compare stars growth across time, starting from October 2020, of chosen repositories.')
        
    ]),
        
    dcc.Tab(label='Repo Percentage Growth', children=[
    
    dcc.Dropdown(
        id='repo-dropdown',
        options=generate_dropdown(), 
        clearable = False,
        value = generate_dropdown()[0]['label']
    ),
    
    dcc.Graph(id='g_repo_graph'),
    
    dcc.Markdown('Choose a repository from the dropdown to see percentage increase of stars, commits and contributors, starting from October 2020.'),
                 
    html.Div(id='dd-output-container')
        ]),
    
])


])
#close app_layout

    
def get_dbConnection():
    return sqlEngine.connect()


#Interval Callbacks

@app.callback(Output('stars_watchers_graph', 'figure'),
              Output('stars_growth_graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    dbc = get_dbConnection()
    repo_df = repo_create_df(dbc)
    #Stars and Watchers
    s_w_df = create_s_w_df(dbc)
    stars_watchers_graph = create_s_w_graph(s_w_df)
    #Stars Growth Comparison
    stars_df = create_stars_df(repo_df)
    stars_growth_graph1 = stars_growth_graph(stars_df)
    return stars_watchers_graph, stars_growth_graph1

    

#Interactive Callbacks
@app.callback(
    dash.dependencies.Output('g_repo_graph', 'figure'),
    [dash.dependencies.Input('repo-dropdown', 'value')])
def update_output(value):
    #return generate_graph(value)
    return generate_graph(value)    



if __name__ == '__main__':
    app.run_server(port=8053,debug=False)
    





