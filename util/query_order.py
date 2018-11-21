#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : query_order.py
# @Author: wu gang
# @Date  : 2018/10/18
# @Desc  : Http请求查询统一订单平台数据:
#          订单列表接口: 业务线从统一订单平台查询订单列表,按照订单开始时间（或创建时间）倒序、分页返回。
# @Contact: 752820344@qq.com

import sys

import getopt
import hashlib
import requests


def genSid(system, phoneId, orderBy, productId, showType, sinceId):
    key = ""
    # sid = system + phoneid + orderby + sinceid + productid + showtype + status + pagesize
    data = ''.join(system + str(phoneId) + str(orderBy) + str(sinceId) + str(productId) + str(showType) + key + '&*^%@%$^#&')
    # 定义MD5
    hmd5 = hashlib.md5()
    # 生成MD5加密字符串
    hmd5.update(data.encode(encoding='UTF-8'))
    # 获取MD5字符串
    sid = hmd5.hexdigest()
    # 将小写字母切换成大写
    sid = sid.upper()
    return sid[4] + sid[1] + sid[16] + sid[9] + sid[19] + sid[30] + sid[28] + sid[22]


def queryByUid(phoneId, productId, showType, sinceId, system="search",  orderBy = 1):
    """
    订单列表接口
    :param phoneId: 必选 	用户id
    :param productId: 可选 	产品id,多个用逗号分隔。
            共18个产品ID：
                0 机票；29 高铁/火车；7 car; 36 hotel;
                17 caffee; 21 22 mall; 34 bus; 41 tour; 9 12 50 pay; 59 62 67 checkin; 60 activity; 66 insure; 75 hbgj；
    :param showType: 可选 	订单展示类型,多个用逗号分隔。
            订单展示状态showType说明:
                - 0待付款订单 （未支付）,
                - 1已取消订单 （取消支付、临时未支付订单、关闭订单）
                - 2未完成订单 （待出行、待发货、邮寄中、服务中、司机已确认、服务开始、部分退票、部分改期、退票待退款）,
                - 3已完成订单 （已出行、已全部退票退款、已收货、服务完成、已全部改期）,
                - 4已评价订单
    :param sinceId: 可选 	分页标记,即订单开始时间（或订单创建时间）。eg：1539832895000 (2018-10-18 11:21:35)
    :param system: 必选 	业务系统, 默认search
    :return: 用户订单数据
    """
    testUrl = "http://43.241.232.202:6790/huoli-order-query/read/getorderlist"
    url = "http://ordercenter.huoli.local/query/huoli-order-query/read/getorderlist"
    payload = ""
    queryDict = {"system": system, "phoneid": phoneId, "orderby": orderBy, "productid": productId, "showtype": showType,
                 "sinceid": sinceId,
                 "sid": genSid(system, phoneId, orderBy, productId, showType, sinceId)}
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", testUrl, data=payload, headers=headers, params=queryDict)
    print("status code = %d, reason = %s, url = %s" % (response.status_code, response.reason, response.url))
    if response.status_code != 200:
        return "no data."
    return response.text


def main(argv):
    phoneId = ''
    productId = ''
    showType = ''
    sinceId = ''
    try:
        shortArgs = 'h:u:p:s:t:'  # 须使用单字母
        longArgs = ["help", "phoneId=", "productId", "showType=", "sinceId="]
        # sys.argv[1:] 过滤掉第一个参数
        opts, args = getopt.getopt(argv[1:], shortArgs, longArgs)
    except getopt.GetoptError:
        print('query_order.py -u <phoneId> -p <productId> -s <showType> -t <sinceId>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('query_order.py -u <phoneId> -p <productId> -s <showType> -t <sinceId>')
            sys.exit()
        elif opt in ("-u", "--phoneId"):
            phoneId = arg
        elif opt in ("-p", "--productId"):
            productId = arg
        elif opt in ("-s", "--showType"):
            showType = arg
        elif opt in ("-t", "--sinceId"):
            sinceId = arg
    text = queryByUid(phoneId, productId, showType, sinceId)
    print("query result : \n " + text)


if __name__ == '__main__':
    main(sys.argv)
