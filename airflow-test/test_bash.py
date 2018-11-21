#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_bash.py
# @Author: wu gang
# @Date  : 2018/9/4
# @Desc  : 
# @Contact: 752820344@qq.com

from airflow import DAG
from airflow.operators.bash_operator import BashOperatorimport

datetime
import datetime

default_args = {'owner': 'wu gang',
                'depends_on_past': False,
                'start_date': datetime.datetime(2019, 9, 4),
                'email': ['wug@133.cn'],
                'email_on_failure': False,
                'email_on_retry': False,
                'retries': 1,
                'retry_delay': datetime.timedelta(minutes=5),
                # 'end_date': datetime(2016, 1, 1),
                }
# 0,10,20,30,40,50 * * * * *

dag = DAG('tutorial', default_args=default_args, schedule_interval='* * * * *')

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

text = '{{ ds }} [%s] has been done' % (dag.dag_id)


