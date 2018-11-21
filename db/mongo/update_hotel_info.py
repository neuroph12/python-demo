#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : update_hotel_info.py
# @Author: wu gang
# @Date  : 2018/11/7
# @Desc  : 更新酒店推荐数据的猜你喜欢展示Url和标签渐变色
# @Contact: 752820344@qq.com

import json
import pymongo

if __name__ == '__main__':
    # 连接数据库
    client = pymongo.MongoClient('localhost', 27017)
    db = client.flight
    db.authenticate("search", "xxx")
    type = 5
    # uid = "15206728"
    # # uid = "46324606"
    collection = db.tipsUserLink
    # cursor = collection.find({"phoneId": uid, "type": type})
    cursor = collection.find({"type": type})

    new_url = "https://cdn.rsscc.cn/ticket/center/images/181106/154529_52O7_1.png"

    old_url = "https://cdn.rsscc.cn/ticket/center/images/181102/144032_917G_1.png"
    for cur in cursor:
        replaceFields = cur["replaceFields"]
        # json_str = json.dumps(replaceFields)
        rf_dict = json.loads(replaceFields)
        url = rf_dict["iconMedium"]
        # print(url)
        if url == old_url:  # 猜你喜欢
            rf_dict["iconSmall"] = new_url
            rf_dict["iconMedium"] = new_url
            rf_dict["iconLarge"] = new_url

            # 如果是猜你喜欢，更改标签的渐变颜色
            tag = rf_dict['tag']
            bgColor = tag['bgcolor']
            if len(bgColor) == 1:
                # bgColor.clear()
                tag["bgcolor"] = (["255, 102, 128, 100", "255, 79, 91, 100"])
                rf_dict["tag"] = tag

                rf_str = json.dumps(rf_dict, ensure_ascii=False)
                # cur["replaceFields"] = rf_str
                # print("start update : %s" % cur)
                query = {"_id": cur["_id"]}
                collection.update_one(query, {"$set": {"replaceFields": rf_str}})
                print("user %s update url done" % cur["_id"])

    print("update job done!")
