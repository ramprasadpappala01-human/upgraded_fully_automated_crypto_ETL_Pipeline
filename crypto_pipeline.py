
from airflow.sdk import dag, task
import sys
from airflow.timetables.interval import DeltaDataIntervalTimetable
from pendulum import datetime, duration
from crypto_pipeline_project.extract import extract_data
from crypto_pipeline_project.transform import transform_data
from crypto_pipeline_project.load import load_data
import pandas as pd
from io import StringIO


@dag(
    dag_id='crypto_pipeline',
    start_date=datetime(2026,5,24,tz='Asia/Kolkata'),
    schedule=DeltaDataIntervalTimetable(duration(minutes=1)),
    is_paused_upon_creation=False,
)
def crypto_pipeline():
    
    @task.python
    def run_extract():
        data=extract_data()
        return data
    @task.python
    def run_transform(data):
        transformed_data=transform_data(data)
        return transformed_data.to_json(orient='records',date_format='iso')
    @task.python
    def run_load(transformed_data):
        df=pd.read_json(StringIO(transformed_data),orient='records')
        df['time_stamp']=pd.to_datetime(df['time_stamp'])
        load_data(df)
    raw=run_extract()
    transformed=run_transform(raw)
    run_load(transformed)

crypto_pipeline()
        
