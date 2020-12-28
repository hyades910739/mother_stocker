from airflow.providers.docker.operators.docker import DockerOperator
from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'eric',
    'depends_on_past': False,
    'email': ['hyades910739@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    'stock_update_with_docker_operator',
    default_args=default_args,
    description='update latest stock price daily.',
    schedule_interval='0 0 * * *',
    start_date=days_ago(2),
    tags=['stock'],
)

task1 = DockerOperator(
    command='price',
    task_id='update_stock_price_by_crawler',
    image= "stock_update",    
    dag=dag,
    do_xcom_push=False
)

task2 = DockerOperator(
    command='stats',
    task_id='update_revenue_stats',
    image= "stock_update",    
    dag=dag,
    do_xcom_push=False
)

task1 >> task2

