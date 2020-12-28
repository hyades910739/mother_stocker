# Mother Stocker
A tiny app used to track and update price of stocks my mom sold or bought.


## What's in it.
1. get records by google spreadsheet API. (spreadsheet is writen and update by my Mom.)
2. update latest price by crawler.
3. calculate how much we LOSE qq.
4. update price and statistics.
5. schedule it by airflow(2.0).


## how to use it with airflow.
1. create your google api credentials. ([guide](https://developers.google.com/sheets/api/quickstart/python))
2. build Dockerfile for stock_update. `docker build -t stock_update .`
3. put `dag_stock_update.py` into `AIRFLOW_HOME` (where you put your DAGs.). 
4. build your airflow environment and run. ([guide](https://airflow.apache.org/docs/apache-airflow/stable/start.html))

