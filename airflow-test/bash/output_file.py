#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : output_file.py
# @Author: wu gang
# @Date  : 2018/9/4
# @Desc  : 
# @Contact: 752820344@qq.com

import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta

default_args = {
    'owner': 'wu gang',
    'start_date': dt.datetime(2018, 9, 4),  # dag会补回之前没运行过时间周期
    'email': ['wug@133.cn'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,  # 在失败任务之前应该执行的重试次数
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG(
        'output_file',
        default_args=default_args,
        schedule_interval='* * * * *',
) as dag:
    output_first = BashOperator(task_id='output_first',
                                bash_command='echo "hello world $(date "+%Y-%m-%d %H:%M:%S")" >> /data/search/test/file.txt')
    sleep = BashOperator(task_id='sleep', bash_command='sleep 5')
    output_end = BashOperator(task_id='output_end',
                              bash_command='echo "$(date "+%Y-%m-%d %H:%M:%S") + ": ---------"" >> /data/search/test/file.txt')

output_first >> sleep >> output_end
