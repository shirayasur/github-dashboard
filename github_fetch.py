#!/usr/bin/env python
# coding: utf-8



from github import Github
import pandas as pd
import datetime
import urllib.request, urllib.parse, urllib.error
import re
from sqlalchemy import create_engine
import pymysql

from config import DB_CONNECTION_STRING, GH_API_TOKEN, REPOS

def open_issues(x,headers):
    try:
        url = f"https://api.github.com/search/issues?q=repo:{x}+type:issue+state:open"
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read().decode()
        num = re.findall('"total_count":([0-9]+)', data)
        return int(num[0])
    except Exception as e:
        print(e)
        return None


def closed_issues(x,headers):
    try:
        url = f"https://api.github.com/search/issues?q=repo:{x}+type:issue+state:closed"
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read().decode()
        num = re.findall('"total_count":([0-9]+)', data)
        return int(num[0])
    except Exception as e:
        print(e)
        return None


def latest_release(x,headers):
    today = datetime.datetime.now()
    try:
        url = f"https://api.github.com/repos/{x}/releases/latest"
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read().decode()
        date = re.findall('"published_at":"(.+?)"', data)
        s_date = date[0]
        real_date = datetime.datetime.strptime(s_date, '%Y-%m-%dT%H:%M:%SZ')
        date_diff = today-real_date
        return real_date.strftime("%b %d, %Y"), int(date_diff.days)
    except Exception as e:
        print(e)
        return (None, None)


def main():
    sqlEngine = create_engine(DB_CONNECTION_STRING, pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    headers = {'Authorization': 'token %s' % GH_API_TOKEN}
    g = Github(GH_API_TOKEN)
    competitors = []
    for x in REPOS:
        repo = g.get_repo(x)
        release_date , days_ago = latest_release(x,headers)
        repo_dict = {"Date" : datetime.datetime.now().strftime("%b %d, %Y"),
            "Repo_Name" : x,
            "Name" : repo.name,
            "Stars" : repo.stargazers_count,
            "Watchers" : repo.subscribers_count,
            "Forks" : repo.forks_count,
            "Open_Issues" : open_issues(x,headers),
            "Closed_Issues" : closed_issues(x,headers),
            "Total_Commits" : repo.get_commits().totalCount,
            "Contributors" : repo.get_contributors().totalCount,
            "Release_Date" : release_date,
            "RL_Days_Ago" : days_ago,
            "Language" : repo.language}
        competitors.append(repo_dict)
    df = pd.DataFrame(competitors)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Release_Date'] = pd.to_datetime(df['Release_Date'])
    df.to_sql("github_table", dbConnection, if_exists='append', index=False)


if __name__ == "__main__":
    main()


