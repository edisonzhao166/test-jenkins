
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
import pandas as pd
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="demo1", start_date=datetime(2022, 1, 1), schedule="@once") as dag:
    # Tasks are represented as operators
    hello = BashOperator(task_id="hello", bash_command="echo hello")

    @task()
    def airflow():
        print("airflow")

    @task()
    def store():
        # Open a file in write mode ('w'), which will create the file if it doesn't exist
        with open('./output.txt', 'w') as file:
            # Write content to the file
            file.write('Hello, this is a line of text.\n')
            file.write('Here is another line.')

    @task()
    def pd_access():
        url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
        df = pd.read_csv(url)
        df.to_csv("./aaa.csv", index=False)


    upload_to_s3 = LocalFilesystemToS3Operator(
        task_id='upload_file_to_s3',
        filename='./output.txt',  # Local file path
        dest_key='your_s3_key/output.txt',  # S3 key (file path in S3)
        dest_bucket='ez2024',  # S3 bucket name
        aws_conn_id='ez2024',  # AWS connection ID in Airflow
        replace=True  # Replace file if it exists
    )


    # Set dependencies between tasks
    hello >> airflow() >> store() >> pd_access() >> upload_to_s3

