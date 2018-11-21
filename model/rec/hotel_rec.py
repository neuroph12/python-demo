#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : hotel_rec.py
# @Author: wu gang
# @Date  : 2018/9/13
# @Desc  : 基于Kaggle的酒店数据，构建酒店推荐引擎
# 参考：A Machine Learning Approach — Building a Hotel Recommendation Engine
# 地址：https://towardsdatascience.com/a-machine-learning-approach-building-a-hotel-recommendation-engine-6812bfd53f50
# @Contact: 752820344@qq.com

import os
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn import svm

if __name__ == '__main__':
    # 读取文件，内容以','分割，用dropna()过滤缺失值；
    df = pd.read_csv('/Users/wugang/datasets/hotel_data/train.csv.gz', sep=',').dropna()
    # destPath = os.path.abspath(os.path.dirname(os.getcwd())) + "/data/hotel/"
    # destPathFile = destPath + 'destinations.csv.gz'
    dest = pd.read_csv('/Users/wugang/datasets/hotel_data/destinations.csv.gz')
    # frac表示抽取数据的百分比; random_state随机种子数
    df = df.sample(frac=0.01, random_state=99)
    # 获得df的size
    df.shape
    # 获得df的行数
    df.shape[0]
    # 获得df的列数
    df.shape[1]
    # 获得df中的值
    # df.values

    # figsize设置画布大小
    plt.figure(figsize=(12, 6))
    sns.distplot(df['hotel_cluster'])
