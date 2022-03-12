#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import datetime
from datetime import date, timedelta   
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import REPOS


#create df
def repo_create_df(dbConnection):
    df = pd.read_sql("select * from github.github_table", dbConnection);
    df['Date'] = pd.to_datetime(df['Date'])
    df['Release_Date'] = pd.to_datetime(df['Release_Date'])
    return df


#Create Stars/Watchers df
def create_s_w_df(dbConnection):
    s_w_df = pd.read_sql("""
    SELECT Name, Watchers, Stars
    FROM github.github_table
    WHERE github_table.Date = (SELECT MAX(github_table.Date) FROM github_table);
    """,dbConnection)
    return s_w_df


#Create GitHub Growth df
def github_growth(df, name):
    growth_df = df[['Name','Date','Stars','Total_Commits','Contributors']]
    growth_df = growth_df[growth_df.Name==name].reset_index()
    growth_df = growth_df.drop('index', axis=1)
    first_star = growth_df.Stars.iloc[0] 
    first_commit = growth_df.Total_Commits.iloc[0]
    first_contributor = growth_df.Contributors.iloc[0]
    pc_stars = growth_df['Stars']/first_star*100
    pc_commits = growth_df['Total_Commits']/first_commit*100
    pc_contributors = growth_df['Contributors']/first_contributor*100
    growth_df.insert(3, "pc_stars", pc_stars, True)
    growth_df.insert(5, "pc_commits", pc_commits, True)
    growth_df.insert(7, "pc_contributors", pc_contributors, True)
    return growth_df

#Create Stars df
def create_stars_df(df):
    stars_df = df[['Date','Name','Stars']] 
    return stars_df

#Create Stars/Watchers graph
def create_s_w_graph(s_w_df):
    name = s_w_df.Name.tolist()
    watchers = s_w_df.Watchers.tolist()
    stars = s_w_df.Stars.tolist()

    fig = go.Figure(data=[
    go.Bar(name='Watchers', x=watchers, y=name, orientation = 'h', marker=dict(color='#90EE90')),
    go.Bar(name='Stars', x=stars, y=name, orientation = 'h', marker=dict(
        color="#FFD700"))
    ])
    fig.update_layout(barmode='stack', title='Repo Stars and Watchers')
    return fig


#Create Percentage Growth Graph
def growth_graph(df):
    stars = df.Stars.tolist()
    commits = df.Total_Commits.tolist()
    contributors = df.Contributors.tolist()
    g_stars = df.pc_stars.tolist()
    g_commits = df.pc_commits.tolist()
    g_contributors = df.pc_contributors.tolist()
    date = df.Date.tolist()
    name = df.Name.iloc[0]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
    go.Scatter(x=date, y=g_stars, name="Stars", text = stars),
    secondary_y=False)

    fig.add_trace(
    go.Scatter(x=date, y=g_commits, name="Commits", text = commits),
    secondary_y=False)
    
    fig.add_trace(
    go.Scatter(x=date, y=g_contributors, name="Contributors", text = contributors),
    secondary_y=False)

    fig.update_layout(
    title_text=f"GitHub Activity Percentage Growth - {name}")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text='Percentage Growth')
    ticks = int((len(date))/4)
    fig.update_xaxes(nticks=ticks)
    return fig


#Create Stars Growth graph
def stars_growth_graph(df):
    fig = px.line(df, x="Date", y='Stars', color = 'Name')
    fig.update_layout(title='Stars Growth')  
    return fig

#Create dropdown for repo names
def get_dropdown_names(dbConnection):
    names = pd.read_sql("select distinct Name from github.github_table", dbConnection).Name.tolist()
    names.sort()
    dropdown_list=[]
    for name in names:
        dropdown_list.append({'label': name, 'value' : name})
    return dropdown_list

