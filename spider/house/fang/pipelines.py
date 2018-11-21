#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : pipelines.py
# @Author: wu gang
# @Date  : 2018/10/22
# @Desc  : 
# @Contact: 752820344@qq.com

import time

import pandas as pd


class HousePipeline(object):
    """
    house_list用于收集每次传递进来的item
    close_spider函数用于指明爬虫结束时进行的操作，函数中把house_list先转化为pandas的DataFrame，
    然后DataFrame转化为excel，最后通过time.process_time() 函数打印程序运行的总时间。
    """
    house_list = []

    def process_item(self, item, spider):
        self.house_list.append(dict(item))
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.house_list)
        df.to_excel("厦门房价数据(房天下版).xlsx", columns=[k for k in self.house_list[0].keys()])
        print("爬虫程序共运行{}秒".format(time.process_time()))
