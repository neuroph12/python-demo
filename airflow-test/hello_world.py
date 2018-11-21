#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : hello_world.py
# @Author: wu gang
# @Date  : 2018/9/4
# @Desc  : 
# @Contact: 752820344@qq.com

import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'wu gang',
    'start_date': dt.datetime(2018, 9, 4),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


def print_world():
    print('world')


with DAG(
        'hello_world',
        default_args=default_args,
        schedule_interval='0 * * * *',
) as dag:
    print_hello = BashOperator(task_id='print_hello', bash_command='echo "hello "')
    sleep = BashOperator(task_id='sleep', bash_command='sleep 5')
    print_world = PythonOperator(task_id='print_world', python_callable=print_world)

print_hello >> sleep >> print_world
