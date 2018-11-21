#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_dag.py
# @Author: wu gang
# @Date  : 2018/9/4
# @Desc  : 
# @Contact: 752820344@qq.com

from __future__ import print_function
import airflow
from airflow.operators.hive_operator import HiveOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG

dw_list = [
    # 基本信息
    '/home/airflow/dw_dm_hiveql/dw/dw_department_p_erp.sql',
    '/home/airflow/dw_dm_hiveql/dw/dw_emp_p_erp.sql',
]

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}


def read_hql_file(filepath):
    hql = ""
    with open(filepath, 'r') as f:
        while 1:
            line = f.readline()
            hql += str(line)
            if not line:
                break
    print("___________")
    print(hql)
    print("_____________________________________________________")
    return hql


args['pool'] = 'pool_dw'  # 单独设置 sub dag 的pool 参数
with DAG(
        # DAG_NAME,
        dag_id='test_dag',
        default_args=args,
        schedule_interval=None,
        description='dw test'
) as dag:
    dummy_dw_mysqlapp = DummyOperator(task_id="DW_Tasks_Start")
    dag >> dummy_dw_mysqlapp
    last_task = dummy_dw_mysqlapp
    for hqlfilepath in dw_list:
        task_id = hqlfilepath.split("/")[-1].split(".")[0]
        print('task_id ', task_id)
        current_task = HiveOperator(
            hive_cli_conn_id='hive_cli_emr',
            task_id=task_id,
            hiveconf_jinja_translate=True,
            hql=read_hql_file(hqlfilepath),
            trigger_rule='all_done',
            dag=dag
        )
        current_task.set_upstream(last_task)
        last_task = current_task
