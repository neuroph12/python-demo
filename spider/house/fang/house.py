#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : house.py
# @Author: wu gang
# @Date  : 2018/10/22
# @Desc  : 爬取房天下厦门的二手房信息
# @Contact: 752820344@qq.com

import json
import scrapy
from scrapy.http import Request

from spider.house.fang.items import HouseItem


class HouseSpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['esf.xm.fang.com']
    start_urls = []
    # python3可以把变量名设置为中文，但必须全部是中文，不能为100万以下这种形式
    region_dict = dict(
        集美="house-a0354",
        翔安="house-a0350",
        同安="house-a0353",
        海沧="house-a0355",
        湖里="house-a0351",
        思明="house-a0352"
    )
    price_dict = dict(
        d100="d2100",
        c100d200="c2100-d2200",
        c200d250="c2200-d2250",
        c250d300="c2250-d2300",
        c300d400="c2300-d2400",
        c400d500="c2400-d2500",
        c500d600="c2500-d2600",
        c600="c2600"
    )

    for region in list(region_dict.keys()):
        for price in list(price_dict.keys()):
            url = "http://esf.xm.fang.com/{}/{}/".format(region_dict[region], price_dict[price])
            start_urls.append(url)

    def parse(self, response):
        """
        start_urls共有48个，parse函数的作用是找出这48个分类中每个分类的最大页数, 通过字符串拼接得到每一页的url。
        每一页的url用yield Request(url, callback=self.parse1)发起请求，并调用parse1函数进行解析
        :param response:
        :return:
        """
        pageNum = response.xpath("//span[@class='txt']/text()").extract()[0].strip('共').strip('页')
        for i in range(1, int(pageNum) + 1):
            url = "{}-i3{}/".format(response.url.strip('/'), i)
            yield Request(url, callback=self.parse1)

    def parse1(self, response):
        """
        parse1函数用于获取每一页30个房价详情页面的url链接，通过yield Request(detailUrl,callback=self.parse2)发起请求，并调用parse2函数进行解析
        :param response:
        :return:
        """
        house_list = response.xpath("//div[@class='houseList']/dl")
        for house in house_list:
            if "list" in house.xpath("@id").extract()[0]:
                detailUrl = "http://esf.xm.fang.com" + house.xpath("dd[1]/p/a/@href").extract()[0]
                yield Request(detailUrl, callback=self.parse2)

    def parse2(self, response):
        """
        确定xpath书写正确，成功获取到字段后，将字段存入item，最后通过yield item交给管道处理。
        :param response:
        :return:
        """

        def find(xpath, pNode=response):
            if len(pNode.xpath(xpath)):
                return pNode.xpath(xpath).extract()[0]
            else:
                return ''

        item = HouseItem()
        item['title'] = find("//h1[@class='title floatl']/text()").strip()
        item['price'] = find("//div[@class='trl-item_top']/div[1]/i/text()") + "万"
        item['downPayment'] = find("//div[@class='trl-item']/text()").strip().strip("首付约 ")
        item['sizeType'] = find("//div[@class='tab-cont-right']/div[2]/div[1]/div[1]/text()").strip()
        item['size'] = find("//div[@class='tab-cont-right']/div[2]/div[2]/div[1]/text()")
        item['unitPrice'] = find("//div[@class='tab-cont-right']/div[2]/div[3]/div[1]/text()")
        item['orientation'] = find("//div[@class='tab-cont-right']/div[3]/div[1]/div[1]/text()")
        item['floor'] = find("//div[@class='tab-cont-right']/div[3]/div[2]/div[1]/text()") + ' ' + \
                        find("//div[@class='tab-cont-right']/div[3]/div[2]/div[2]/text()")
        item['decoration'] = find("//div[@class='tab-cont-right']/div[3]/div[3]/div[1]/text()")
        item['community'] = find("//div[@class='tab-cont-right']/div[4]/div[1]/div[2]/a/text()")
        item['region'] = find("//div[@class='tab-cont-right']/div[4]/div[2]/div[2]/a[1]/text()").strip() + \
                         '-' + find("//div[@class='tab-cont-right']/div[4]/div[2]/div[2]/a[2]/text()").strip()
        item['school'] = find("//div[@class='tab-cont-right']/div[4]/div[3]/div[2]/a[1]/text()")
        detail_list = response.xpath("//div[@class='content-item fydes-item']/div[2]/div")
        detail_dict = {}
        for detail in detail_list:
            key = find("span[1]/text()", detail)
            value = find("span[2]/text()", detail).strip()
            detail_dict[key] = value
        item['houseDetail'] = json.dumps(detail_dict, ensure_ascii=False)
        item['keySellingPoint'] = '\n'.join(
            response.xpath("//div[text()='核心卖点']/../div[2]/div/text()").extract()).strip()
        item['equipment'] = '\n'.join(response.xpath("//div[text()='小区配套']/../div[2]/text()").extract()).strip()
        yield item
