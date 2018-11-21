#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : copy_data.py
# @Author: wu gang
# @Date  : 2018/11/13
# @Desc  : MongoDB将数据跨服务器复制备份
# @Contact: 752820344@qq.com
import time

import pymongo


def timestamp_from_objectid(objectid):
  ''' ObjectId convert timestamp '''
  result = 0
  try:
    result = time.mktime(objectid.generation_time.timetuple())#get timestamp
  except:
    pass
  return result


if __name__ == '__main__':
    # 连接数据库
    client = pymongo.MongoClient('localhost', 27017)
    # client = pymongo.MongoClient('123.56.222.127', 27017) # test
    db = client.flight
    db.authenticate("search", "xxx")
    collection = db.tips
    cursor = collection.find()
    for cur in cursor:
        _id = cur["_id"]
        print(_id)
        print(timestamp_from_objectid(cur["_id"]))
        # print(tip)
        # t = json.dumps(tip, ensure_ascii=False)
        # print(t)

