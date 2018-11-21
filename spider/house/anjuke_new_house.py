#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : anjuke_new_house.py
# @Author: wu gang
# @Date  : 2018/10/19
# @Desc  : 爬取安居客上南京新房价格：
#           https://nj.fang.anjuke.com/?from=AF_Home_switchcity
#           注意：安居客反爬虫会封IP，需改为动态代理
# @Contact: 752820344@qq.com

import time

import pandas
import random
import requests
from bs4 import BeautifulSoup

headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive',
           'Referer': 'http://www.baidu.com/'
           }


def getIpList():
    """
    只采集了一页的IP
    """
    url = 'http://www.xicidaili.com/nn/'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    ips = soup.find(id='ip_list').find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def getRandomIp(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    print("set proxies = %s" % proxies)
    return proxies


def crawl(url):
    proxies = getRandomIp(getIpList())
    request = requests.get(url, headers=headers, proxies=proxies)
    request.encoding = 'utf-8'
    soup = BeautifulSoup(request.text, 'lxml')  # 使用lxml解析器
    houses = soup.select('.item-mod')[4:]  # 过滤前3个标签
    houseDetails = []
    for house in houses:
        # 获取楼盘名字
        houseName = house.select('.items-name')[0].text
        # 价格
        priceBefore = house.select('.price')
        if len(priceBefore) == 0:
            priceBefore = house.select('.price-txt')
        price = priceBefore[0].text
        # 地址
        address = house.select('.list-map')[0].text
        if (address[-1] == '.'):
            href = house.select('.pic')[0]['href']
            request = requests.get(href)
            if request.status_code == 200:
                request.encoding = 'utf-8'
                soup = BeautifulSoup(request.text, 'lxml')
                address = soup.select('.lpAddr-text')[0].text
            else:
                print("parse address error, status_code %s" % request.status_code)
        # 面积
        houseSizeBefore = house.select('.huxing span')
        if (len(houseSizeBefore) > 0):
            houseSize = houseSizeBefore[-1].text
        else:
            houseSize = ''
        # 销售状态
        saleStatus = house.select('.tag-panel i')[0].text
        # 户型
        if (len(house.select('.tag-panel i')) == 2):
            houseType = house.select('.tag-panel i')[1].text
        else:
            houseType = house.select('.tag-panel span')[0].text

        # 将获取的信息做成房屋信息字典
        houseDetail = {}
        houseDetail['houseName'] = houseName
        houseDetail['price'] = price
        houseDetail['address'] = address
        houseDetail['houseSize'] = houseSize
        houseDetail['saleStatus'] = saleStatus
        houseDetail['houseType'] = houseType
        print(houseDetail)
        houseDetails.append(houseDetail)
    return houseDetails


def crawlAll(url, endPageNum):
    """
    爬取所有的信息
    :param url: 基础url地址，如：'https://nj.fang.anjuke.com/loupan/all/p{}/'
    :param endPageNum: 结束页码，具体观察网站
    :return:
    """
    allHouseDetails = []
    for i in range(1, endPageNum + 1):
        time.sleep(5)
        pageUrl = url.format(i)
        print("start crawl page %d, url: %s" % (i, pageUrl))
        allHouseDetails.extend(crawl(pageUrl))
    print("total count %d" % len(allHouseDetails))
    dataFrame = pandas.DataFrame(allHouseDetails)
    return dataFrame


if __name__ == '__main__':
    url = 'https://xm.fang.anjuke.com/loupan/all/p{}/'
    # 安居客上南京新房页数共34页，每页30个
    allHouseDetails = crawlAll(url, 34)
    allHouseDetails.to_excel("anjukeXMNewHouse.xlsx")
    print(allHouseDetails.head(10))
