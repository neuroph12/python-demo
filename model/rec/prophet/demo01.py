#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : demo01.py
# @Author: wu gang
# @Date  : 2018/10/26
# @Desc  : 
# @Contact: 752820344@qq.com

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fbprophet import Prophet

"""
如何利用Prophet构建有效的预测模型:
- 首先我们去除数据中的异常点（outlier），直接赋值为none就可以，因为Prophet的设计中可以通过插值处理缺失值，但是对异常值比较敏感。
- 选择趋势模型，默认使用分段线性的趋势，但是如果认为模型的趋势是按照log函数方式增长的，可设置growth='logistic'从而使用分段log的增长方式
- 设置趋势转折点（changepoint），如果我们知道时间序列的趋势会在某些位置发现转变，可以进行人工设置，比如某一天有新产品上线会影响我们的走势，我们可以将这个时刻设置为转折点。
- 设置周期性，模型默认是带有年和星期以及天的周期性，其他月、小时的周期性需要自己根据数据的特征进行设置，或者设置将年和星期等周期关闭。
- 设置节假日特征，如果我们的数据存在节假日的突增或者突降，我们可以设置holiday参数来进行调节，可以设置不同的holiday，例如五一一种，国庆一种，影响大小不一样，时间段也不一样。
- 此时可以简单的进行作图观察，然后可以根据经验继续调节上述模型参数，同时根据模型是否过拟合以及对什么成分过拟合，我们可以对应调节seasonality_prior_scale、holidays_prior_scale、changepoint_prior_scale参数。
"""


def test01():
    file_name = "../../../data/prophet/example_retail_sales.csv"
    df = pd.read_csv(file_name)
    df['y'] = np.log(df['y'])
    df.head()
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    future.tail()
    forecast = m.predict(future)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
    m.plot(forecast)
    x1 = forecast['ds']
    y1 = forecast['yhat']
    plt.plot(x1, y1)
    plt.show()


def test02():
    """
    参考：https://blog.csdn.net/wjskeepmaking/article/details/64905745
    """
    file_path = '../../../data/prophet/example_wp_peyton_manning.csv'
    # 使用pandas的read_csv()方法读取数据，返回的结果df是一个DataFrame格式的对象，
    # 打印df可以看到类似于以下数据格式（ds和y是必须的，不能改变）：
    df = pd.read_csv(file_path)
    # print(df) # 2905个

    # 创建一个Prophet对象
    m = Prophet()

    # 先求对数（以e为底）
    df['y'] = np.log(df['y'])  # 计算各元素的自然对数为底的对数
    print(df['y'])  # 从df中取出y字段对应的列值2905个
    # print(df)

    # 填充数据，训练模型
    m.fit(df)

    # 构建预测集
    # 参数：periods, freq='D', include_history=True
    # - periods: 指定要预测的时长，要根据freq这个参数去设置。假如freq='D'，那么粒度为天，periods则指定要预测未来多少天的数据。
    #       如果freq='H‘,则periods指定要预测未来多少小时的数据（当然，要在框架支持粒度为小时的前提下才能运用）
    # - freq='D': 默认 freq='D'，那么粒度为天
    # - include_history=True: include_history：是否包含历史数据，保持默认就好。
    future = m.make_future_dataframe(freq='D', periods=2)

    # 预测
    """
    预测好的数据是返回给forescasts,如果上一步的include_history传入为False，那么这次的返回将不会包括里历史数据。只包含预测出来的数据。 
    """
    forecasts = m.predict(future)

    print(forecasts.tail(10))
    forecasts[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10)
    m.plot(forecasts)
    plt.show()

    # 画图
    """
    默认会画出趋势、年周期、星期周期成分（如果在定义模型时给出了holiday参数，还会做出holiday的成分图）
    其中蓝色线为预测结果，黑色点为原数据点。除此之外，由于Prophet使用的是加性模型，也就是把模型分为趋势模型、周期模型、节假日以及随机噪声的叠加。
    """
    m.plot(forecasts).show()
    m.plot_components(forecasts).show()  # 利用m.plot_components(forecast)，对各个成分进行作图观察


if __name__ == '__main__':
    test02()
