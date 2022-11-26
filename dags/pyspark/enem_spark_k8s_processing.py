from airflow.models import Variable
import boto3
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


aws_access_key_id = Variable.get('aws_access_key_id')
aws_secret_access_key = Variable.get('aws_secret_access_key')
glue = boto3.client(
    'glue',
    region_name='us-east-2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)


from airflow.utils.dates import days_ago


def trigger_crawler_func():
    glue.start_crawler(Name='enade_crawler')


with DAG(
    'enade_batch_spark_k8s',
    default_args={
        'owner': 'Gabs',
        'depends_on_past': False,
        'email': ['gabriel.okazaki@hotmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'max_active_runs': 1
    },
    description='submit spark-pi as sparkApplication on kubernetes',
    schedule_interval='0 */2 * * *',
    start_date=days_ago(1),
    catchup=False,
    tags=['spark', 'kubernetes', 'batch', 'enem']
) as dag:
    converte_parquet = SparkKubernetesOperator(
        task_id='converte_parquet',
        namespace='airflow',
        application_file='enem_converte_parquet.yaml',
        kubernetes_conn_id="kubernetes_default",
        do_xcom_push=True
    )

    converte_parquet_monitor = SparkKubernetesSensor(
        task_id='converte_parquet_monitor',
        namespace='airflow',
        application_name="{{ task_instance.xcom_pull(task_ids='converte_parquet')['metadata']['name'] }}",
        kubernetes_conn_id="kubernetes_default"
    )

    trigger_crawler = PythonOperator(
        task_id='trigger_crawler',
        python_callable=trigger_crawler_func
    )

converte_parquet >> converte_parquet_monitor >> trigger_crawler