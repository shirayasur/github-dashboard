# Github Repos Tracker 
 A dashboard that tracks metrics of multiple repositories such as stars, watchers and contributors over time

## About
This dashboard tracks repository metrics to compare between various open source projects using the Github API.

It tracks number of stars and watchers, compares stars growth between various repos, as well as commits and contributors.

Since Github does not provide historical data, this dashboard makes periodic API requests and stores data in a mySQL database. 

See screenshots [here](https://github.com/shirayasur/github_dashboard/tree/main/screenshots)

![screenshot_3](https://github.com/shirayasur/github_dashboard/blob/main/screenshots/screenshot_3.png)

## How to Use
1. Set up a mySQL database and run `create_db.sql` into a new database
2. Plug your mySQL connection string in `config.py` (DB_CONNECTION_STRING)
3. Insert your Github API key in `config.py` (GH_API_TOKEN)
4. Select the github repositories you would like to track and insert them into `config.py` (REPOS)
5. Create a schedule run for `github_fetch.py` e.g. using [crontab](https://crontab.guru)
6. Run `github_dashboard.py` to activate dashboard (default port is set to 8053)

### Other Options
`interval` (github_dashboard.py) - change this to set how often the dashboard should refresh the data. Default is every 12 hours.

