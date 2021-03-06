import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Following are defaults which can be overridden later on
default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2022, 4, 23),
    'email': ['mark@coder.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('datafile', default_args=default_args)


def task_read_la_911_2021_data():
  print("reading data from Los Angeles 911 activity")
  la_911_data=pd.read_json("https://data.lacity.org/resource/cibt-wiru.json")
  la_911_data.to_csv("/home/coder/la_911_2021_data.csv")

def task_read_la_911_2020_data():
  print("reading data from Los Angeles 911 activity")
  la_911_data=pd.read_json("https://data.lacity.org/resource/84iq-i2r6.json")
  la_911_data.to_csv("/home/coder/la_911_2020_data.csv")

 
def task_merge():
   print("2021 911 call types")
   data_2021=pd.read_csv('/home/coder/la_911_2021_data.csv')
   calltype_2021=data_2021['call_type_text'].value_counts(sort=True, ascending=True).to_frame()
   calltype_2021.to_csv('/home/coder/la_911_2021_calltypes.csv')
   area_occ_2021=data_2021['area_occ'].value_counts(sort=True, ascending=True).to_frame()
   area_occ_2021.to_csv('/home/coder/la_911_2021_area_occ.csv')
   print("2020 911 call types")
   data_2020=pd.read_csv('/home/coder/la_911_2020_data.csv')
   calltype_2020=data_2021['call_type_text'].value_counts(sort=True, ascending=True).to_frame()
   calltype_2020.to_csv('/home/coder/la_911_2020_calltypes.csv')
   area_occ_2020=data_2020['area_occ'].value_counts(sort=True, ascending=True).to_frame()
   area_occ_2020.to_csv('/home/coder/la_911_2020_area_occ.csv')   
   m=pd.concat([calltype_2021,calltype_2020],axis=1)
   m.columns=['year2021','year2020']
   m.to_csv('/home/coder/la_911_2021_2020_calltypes.csv')
   m=pd.concat([area_occ_2021,area_occ_2020],axis=1)
   m.columns=['year2021','year2020']
   m.to_csv('/home/coder/la_911_2021_2020_area_occ.csv')   


t1 = PythonOperator(
    task_id='read_json_2021',
    python_callable=task_read_la_911_2021_data,
    dag=dag)

t2 = PythonOperator(
    task_id='read_json_2020',
    python_callable=task_read_la_911_2020_data,
    dag=dag)

t3 = PythonOperator(
    task_id='merge',
    python_callable=task_merge,
    dag=dag)

t3.set_upstream(t1)
t3.set_upstream(t2)