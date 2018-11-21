#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : mongo_update.py
# @Author: wu gang
# @Date  : 2018/11/3
# @Desc  :  更新mongodb数据库中的表字段信息
# @Contact: 752820344@qq.com

import pymongo
import json

if __name__ == '__main__':
    # 连接数据库
    client = pymongo.MongoClient('localhost', 27017)
    db = client.flight
    db.authenticate("search", "xxx")
    type = 5
    collection = db.tipsUserLink
    cursor = collection.find({"type": type})

    new_url_1 = "https://cdn.rsscc.cn/ticket/center/images/181102/144040_T471_1.png"
    new_url_2 = "https://cdn.rsscc.cn/ticket/center/images/181102/144032_917G_1.png"

    old_url_1 = "https://cdn.rsscc.cn/ticket/center/images/181023/140629_925M_1.png"
    old_url_2 = "https://cdn.rsscc.cn/ticket/center/images/181023/140649_490T_1.png"
    for cur in cursor:
        replaceFields = cur["replaceFields"]
        # json_str = json.dumps(replaceFields)
        rf_dict = json.loads(replaceFields)
        url = rf_dict["iconMedium"]
        # print(url)
        if url == old_url_1:  # 曾经预定
            rf_dict["iconSmall"] = new_url_1
            rf_dict["iconMedium"] = new_url_1
            rf_dict["iconLarge"] = new_url_1

            rf_str = json.dumps(rf_dict)
            cur["replaceFields"] = rf_str
            # print("start update : %s" % cur)
            query = {"_id": cur["_id"]}
            collection.update_one(query, {"$set": {"replaceFields": rf_str}})
            print("update %s done" % cur["_id"])

            collection.update_one(query, {"$set": {"replaceFields": rf_str}})
            print("update %s done" % cur["_id"])
        elif url == old_url_2:  # 猜你喜欢
            rf_dict["iconSmall"] = new_url_2
            rf_dict["iconMedium"] = new_url_2
            rf_dict["iconLarge"] = new_url_2

            rf_str = json.dumps(rf_dict)
            cur["replaceFields"] = rf_str
            print("start update : %s" % cur)
            query = {"_id": cur["_id"]}
            collection.update_one(query, {"$set": {"replaceFields": rf_str}})
            print("update %s done" % cur["_id"])

    print("update job done!")



# db.tipsUserLink.insert({
#     "_id" : "46324606531010421538536200000",
#     "sourceId" : "531010420000000000000000",
#     "type" : 5,
#     "phoneId" : "46324606",
#     "updateTime" : 1540282318393,
#     "createTime" : 1540282318393,
#     "label" : "order",
#     "reason" : "基于机票订单的酒店推荐",
#     "weight" : 5,
#     "extra" : "{\"addTime\":\"2018-10-23T16:11:58.394\"}",
#     "price" : 352.11,
#     "oldprice" : 363.0,
#     "expirationTime" : "2018-11-05T03:11:00.000Z",
#     "replaceFields" : "{\"tag\": {\"bgcolor\": [\"255,102,128,1\"], \"text\": \"\\u731c\\u4f60\\u559c\\u6b22\", \"color\": \"255,255,255,1\"}, \"iconSmall\": \"https://cdn.rsscc.cn/ticket/center/images/181102/144032_917G_1.png\", \"iconMedium\": \"https://cdn.rsscc.cn/ticket/center/images/181102/144032_917G_1.png\", \"url\": \"https://hotel.rsscc.cn/detailVue.html?from=hbgj&indexPage=weex&naviBarHidden=1&&hotelId=43101068&modprice=-1&modtype=1&modvalue=0.02\", \"iconLarge\": \"https://cdn.rsscc.cn/ticket/center/images/181102/144032_917G_1.png\", \"tailTag\": [{\"text\": \"\\u9ad8\\u6863\\u578b\", \"color\": \"255,62,74,1\", \"bdcolor\": \"255,62,74,1\"}], \"bgColor\": \"255,247,240,1\"}"
# });

# { "_id" : "46324606409010391541306400000", "sourceId" : "409010390000000000000000", "type" : 5, "phoneId" : "46324606", "updateTime" : 1540821700380, "createTime" : 1540821700380, "label" : "order", "reason" : "基于机票订单的酒店推荐", "weight" : 5, "extra" : "{\"addTime\":\"2018-10-29T22:01:40.380\"}", "price" : 199.68, "oldprice" : 208, "expirationTime" : "2018-11-04T10:40:00Z", "replaceFields" : "{\"iconLarge\": \"https://cdn.rsscc.cn/ticket/center/images/181102/144032_917G_1.png\", \"bgColor\": \"255,247,240,1\", \"iconSmall\": \"https://cdn.rsscc.cn/ticket/center/images/181102/144032_917G_1.png\", \"tailTag\": [{\"color\": \"255,62,74,1\", \"bdcolor\": \"255,62,74,1\", \"text\": \"\\u56db\\u661f\\u7ea7\"}], \"url\": \"https://hotel.rsscc.cn/detailVue.html?from=hbgj&indexPage=weex&naviBarHidden=1&&hotelId=40901039&modprice=-1&modtype=1&modvalue=0.04\", \"iconMedium\": \"https://cdn.rsscc.cn/ticket/center/images/181102/144032_917G_1.png\", \"tag\": {\"color\": \"255,255,255,1\", \"text\": \"\\u731c\\u4f60\\u559c\\u6b22\", \"bgcolor\": [\"255,102,128,1\"]}}" }