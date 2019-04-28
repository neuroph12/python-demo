#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : connect_mongo.py
# @Author: wu gang
# @Date  : 2019/4/28
# @Desc  : 
# @Contact: 752820344@qq.com

from pyspark.sql import SparkSession

if __name__ == '__main__':
    mongodb_url = "mongodb://xx:haha%40qq.com@123.56.xx.xxx/tips."
    spark = SparkSession \
        .builder \
        .appName("Connect MongoDB") \
        .config("spark.mongodb.input.uri", mongodb_url + "carBasicData") \
        .config("spark.mongodb.output.uri", mongodb_url + "carBasicData") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.2.0")\
        .getOrCreate()
    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    df.show(truncate=False)
