#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : mongo.py
# @Author: wu gang
# @Date  : 2018/8/31
# @Desc  : 
# @Contact: 752820344@qq.com

import datetime
from pymongo import MongoClient
from dateutil import tz


if __name__ == '__main__':
    client = MongoClient("localhost", 27017)
    db = client.flight
    db.authenticate("search", "xxx")

    # 查看全部表名称
    db.collection_names()
    print(db.collection_names())

    # 连接表
    collection = db.expire
    # 创建TTL索引，到过期时间自动删除数据
    # collection.create_index([("time", pymongo.ASCENDING)], expireAfterSeconds=60)
    data = {
        "one": 1,
        "two": 235,
        "time": datetime.datetime.utcnow()
    }
    print("now utc time: ", datetime.datetime.utcnow())
    collection.insert(data)
    data2 = {
        "one": 1,
        "two": 235,
        "time": datetime.datetime.utcnow() + datetime.timedelta(seconds=66)
    }
    print("now utc time: ", datetime.datetime.utcnow() + datetime.timedelta(seconds=66))
    collection.insert(data2)

    localTime = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    data3 = {
        "one": 1,
        "two": 235,
        "time": localTime
    }
    print("now local time: ", localTime)
    collection.insert(data3)

    # utc 转为本地时间
    timenow = (datetime.datetime.utcnow() + datetime.timedelta(hours=8))
    timetext = timenow.strftime('%y%m%d')
    print("{} -> {}", timenow, timetext)

    # UTC Zone
    from_zone = tz.gettz('UTC')
    # China Zone
    to_zone = tz.gettz('CST')

    utc = datetime.datetime.utcnow()
    # Tell the datetime object that it's in UTC time zone
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    local = utc.astimezone(to_zone)
    print(local)


# 线上环境
def get_collections():
    client = MongoClient("localhost", 27017)
    db = client.flight
    db.authenticate("search", "xxx")

    # 查看全部表名称
    db.collection_names()
    print(db.collection_names())
