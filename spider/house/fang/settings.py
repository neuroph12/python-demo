#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : settings.py
# @Author: wu gang
# @Date  : 2018/10/22
# @Desc  : 
# @Contact: 752820344@qq.com

BOT_NAME = 'XiaMenHouse'
SPIDER_MODULES = ['spider.house.fang']
NEWSPIDER_MODULE = 'spider.house.fang'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 96
ITEM_PIPELINES = {
    'spider.house.fang.pipelines.HousePipeline': 300,
}