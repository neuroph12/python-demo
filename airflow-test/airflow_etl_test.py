#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : airflow_etl_test.py
# @Author: wu gang
# @Date  : 2018/9/4
# @Desc  : 
# @Contact: 752820344@qq.com

from airflow.operators import ShortCircuitOperator, BashOperator, DummyOperator
from airflow.models import DAG
from datetime import datetime, timedelta
import random
import os

seven_days_ago = datetime.combine(datetime.today() - timedelta(0),
                                  datetime.min.time())
args = {
    'owner': 'airflow',
    'start_date': seven_days_ago,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='airflow_etl_test',
    default_args=args,
    schedule_interval="* * * * *")

cmd = 'ls -l'
run_this_first = DummyOperator(task_id='run_this_first', dag=dag)

# Define ld variables
task_name_ld = "/home/etl/APP/UPCSS/LD"
# Define sp variables
task_name_sp = "/home/etl/APP/UPCSS/SP"
# Define ul variables
task_name_ul = "/home/etl/APP/UPCSS/UL"

# The contents of the sp directory
options = os.listdir(task_name_sp)

branching = ShortCircuitOperator(
    task_id='branching',
    python_callable=lambda: random.choice(options),
    dag=dag)
branching.set_upstream(run_this_first)

join = DummyOperator(
    task_id='join',
    trigger_rule='all_success',
    dag=dag
)

for option in options:

    # Get ld file path
    file_path_ld = task_name_ld + '/' + option + '/bin/'
    # The contents of the obtained file_path_ld directory
    file_names_ld = os.listdir(file_path_ld)

    # Get sp file path
    file_path_sp = task_name_sp + '/' + option + '/bin/'
    # The contents of the obtained file_path_sp directory
    file_names_sp = os.listdir(file_path_sp)

    # Get ul file path
    file_path_ul = task_name_ul + '/' + option + '/bin/'
    # The contents of the obtained file_path_ul directory
    file_names_ul = os.listdir(file_path_ul)
    # Loop to get sp each file name
    for file_name_sp in file_names_sp:
        if os.path.isfile(file_path_sp + file_name_sp):
            task_option_path = '/usr/bin/perl ' + task_name_sp + '/' + option + '/bin/' + file_name_sp + ' '
            task_option_path_ld = '/usr/bin/perl ' + task_name_ld + '/' + option + '/bin/StructuralLoad.pl '
            t = BashOperator(task_id='LD_' + option, bash_command=task_option_path_ld, dag=dag)
            t.set_upstream(branching)
            dummy_follow = BashOperator(task_id='SP_' + option, bash_command=task_option_path, dag=dag)
            t.set_downstream(dummy_follow)
            dummy_follow.set_downstream(join)
    # Loop to get ul each file name
    for file_name_ul in file_names_ul:
        if os.path.isfile(file_path_ul + file_name_ul):
            task_option_path = '/usr/bin/perl ' + task_name_ul + '/' + option + '/bin/' + file_name_ul + ' '
            dummy_follow = BashOperator(task_id='UL_' + option, bash_command=task_option_path, dag=dag)
            dummy_follow.set_upstream(branching)
            dummy_follow.set_downstream(join)
