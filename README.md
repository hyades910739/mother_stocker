# Mother Stocker
幫老母寫的股票追蹤程式。  
(english README: ([here](https://github.com/hyades910739/mother_stocker/blob/master/README_en.md]))
## 在幹嘛
1. 用 google spreadsheet API 抓老母的股票買賣紀錄
2. 用爬蟲更新最新價格
3. 算一算虧了多少錢qq
4. 用 google spreadsheet API 更新
5. 用 airflow 排程定期更新


## airflow 怎麼用
1. 創google api的 credentials ([教學](https://developers.google.com/sheets/api/quickstart/python))
2. build Dockerfile. `docker build -t stock_update .`
3. 把 `dag_stock_update.py` 放到 `AIRFLOW_HOME` 位置 (預設放DAGs的位置)
4. airflow 開起來 ([教學](https://airflow.apache.org/docs/apache-airflow/stable/start.html))
