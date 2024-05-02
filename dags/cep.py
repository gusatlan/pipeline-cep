from func_utils import get_files, uncompress, file_lowercase
from func_cep import ingest_all, ingest_logradouro
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.models import Variable


INPUT_DIR = Variable.get('INPUT_DATA')
CEP_FILE = Variable.get('CEP_FILE')
OUTPUT_DIR = Variable.get('DATA_PATH')


@dag(catchup=False, start_date=datetime(2024, 4, 27), schedule_interval='@daily', template_searchpath='/opt/airflow/sql')
def cep_dag():

    @task
    def print_args(**kargs):
        print(kargs)

    schema_db = PostgresOperator(
        task_id='schema_db',
        postgres_conn_id='postgres_cep',
        sql='cep_schema.sql'
    )


    @task(execution_timeout=timedelta(minutes=20))
    def unzip_files():
        print(f"Timeout for unzip_files(): {timedelta(minutes=20)}")
        zip_files = get_files(INPUT_DIR, CEP_FILE)
        [uncompress(f"{INPUT_DIR}/{file}", "*", f"{OUTPUT_DIR}") for file in zip_files]


    delete_unecessary_files = BashOperator(
        task_id='delete_unecessary_files',
        bash_command=f"rm {OUTPUT_DIR}/cep/*;rm -Rvf {OUTPUT_DIR}/cep/Fixo"
    )

    delete_output_cep = BashOperator(
        task_id='delete_output_cep',
        bash_command=f"rm -R {OUTPUT_DIR}/cep"
    )


    lower_directory = BashOperator(
        task_id='lower_directory',
        bash_command=f"mv {OUTPUT_DIR}/cep/Delimitado/* {OUTPUT_DIR}/cep/;rm -Rvf {OUTPUT_DIR}/cep/Delimitado"
    )

    @task
    def lowercase():
        files = get_files(f'{OUTPUT_DIR}/cep', "")
        [file_lowercase(f'{OUTPUT_DIR}/cep', file) for file in files]

 
    @task
    def etl_1():
        ingest_all(root_path=f'{OUTPUT_DIR}/cep')


    @task
    def etl_2():
        ingest_logradouro(root_path=f'{OUTPUT_DIR}/cep', index_stage=0)


    @task
    def etl_3():
        ingest_logradouro(root_path=f'{OUTPUT_DIR}/cep', index_stage=1)


    @task
    def etl_4():
        ingest_logradouro(root_path=f'{OUTPUT_DIR}/cep', index_stage=2)


    @task
    def etl_5():
        ingest_logradouro(root_path=f'{OUTPUT_DIR}/cep', index_stage=3)


    print_args() >> unzip_files() >> delete_unecessary_files >> lower_directory >> lowercase() >> schema_db >> etl_1() >> etl_2() >> etl_3() >> etl_4() >> etl_5() >> delete_output_cep

cep_dag()

