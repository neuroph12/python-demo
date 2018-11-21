#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : pipeline_definition_demo.py
# @Author: wu gang
# @Date  : 2018/9/3
# @Desc  : Airflow DAG脚本管道定义的示例
# @Contact: 752820344@qq.com

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# 参数定义: 任务必须包含或继承参数task_id和owner
default_args = {
    'owner': 'wugang',
    'depends_on_past': False,
    'start_date': datetime(2018, 9, 3),  # DAGs都有个参数start_date，表示调度器调度的起始时间
    'email': ['wug@133.cn'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,  # 在失败任务之前应该执行的重试次数
    'retry_delay': timedelta(minutes=5),  # 重试的延迟
    # 'queue': 'bash_queue', # 运行此作业时要排队的队列。并非所有执行程序都实现队列管理，CeleryExecutor确实支持定位特定队列。
    # 'pool': 'backfill', # 在此任务应该运行的插槽池中，插槽池是限制某些任务的并发性的一种方法
    # 'priority_weight': 10, # 此任务对其他任务的优先权重。这允许执行程序在事情得到备份时在其他任务之前触发更高优先级的任务。
    # 'end_date': datetime(2016, 1, 1), # 如果指定，调度程序将不会超出此日期
}

# 任务所附的dag的引用, DAG定义1天的schedule_interval
# DAG id 'tutorial'必须在airflow中是unique的, 一般与文件名相同
dag = DAG('tutorial', default_args=default_args, schedule_interval=timedelta(1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
# t1，t2和t3是通过实例化运算符创建的任务的示例
t1 = BashOperator(
    task_id='print_date',  # 用来区分任务
    bash_command='date',
    dag=dag
)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag
)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag
)

t2.set_upstream(t1)

# This means that t2 will depend on t1
# running successfully to run
# It is equivalent to
# t1.set_downstream(t2)

t3.set_upstream(t1)

# all of this is equivalent to
# dag.set_dependency('print_date', 'sleep')
# dag.set_dependency('print_date', 'templated')
