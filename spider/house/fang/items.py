#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : items.py
# @Author: wu gang
# @Date  : 2018/10/22
# @Desc  : 
# @Contact: 752820344@qq.com

import scrapy
from scrapy import Field


class HouseItem(scrapy.Item):
    title = Field()
    price = Field()
    downPayment = Field()
    monthInstallment = Field()
    sizeType = Field()
    size = Field()
    unitPrice = Field()
    orientation = Field()
    floor = Field()
    decoration = Field()
    community = Field()
    region = Field()
    school = Field()
    houseDetail = Field()
    keySellingPoint = Field()
    equipment = Field()