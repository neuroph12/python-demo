#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : get_path.py
# @Author: wu gang
# @Date  : 2018/9/13
# @Desc  : 
# @Contact: 752820344@qq.com

import os

if __name__ == '__main__':
    print('***获取当前目录***')
    print(os.getcwd())
    print(os.path.abspath(os.path.dirname(__file__)))

    print('***获取上级目录***')
    print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    print(os.path.abspath(os.path.dirname(os.getcwd())))
    print(os.path.abspath(os.path.join(os.getcwd(), "..")))

    print('***获取上上级目录***')
    print(os.path.abspath(os.path.join(os.getcwd(), "../..")))

    path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    path = path + "/data/wechat" + '/' + str("test")
    print("新建文件夹：", path)
    # os.mkdir(path)
