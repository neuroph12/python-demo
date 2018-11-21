#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : flight_price_prediction.py
# @Author: wu gang
# @Date  : 2018/10/26
# @Desc  : 基于facebook的Prophet预测模型的机票价格趋势预测
# @Contact: 752820344@qq.com

import sys
import time

import pandas as pd
from fbprophet import Prophet
from io import *
from pymongo import MongoClient


def createStringIO(priceMap):
    valueIO = StringIO()
    valueIO.write('ds,y\n')
    entries = list(priceMap.items())
    entries.sort()
    for ds, y in entries:
        valueIO.write(ds + ',' + str(y) + '\n')
    return StringIO(valueIO.getvalue())


def getCapAndFloor(df):
    maxy = sys.maxsize
    miny = -1 * sys.maxsize
    while True:
        maxy = df.loc[df['y'] != None, 'y'].max()  # 将各个列的值求和，得到的数值作为一新行
        print("maxy=" + str(maxy))
        if maxy > 0 and len(df.loc[df['y'] >= (maxy * 0.8), 'y']) < 10:
            df.loc[df['y'] == maxy, 'y'] = None
        else:
            break
    while True:
        miny = df.loc[df['y'] != None, 'y'].min()
        print("miny=" + str(miny))
        if miny > 0 and len(df.loc[df['y'] <= (miny * 1.2), 'y']) < 10:
            df.loc[df['y'] == miny, 'y'] = None
        else:
            break
    capAndFloor = [df.loc[df['y'] != None, 'y'].max(), df.loc[df['y'] != None, 'y'].min()]
    return capAndFloor


if __name__ == '__main__':
    client = MongoClient("120.133.0.172:27017", authSource="flight", username='search', password='search@huoli123',
                         authMechanism='MONGODB-CR')
    queryId = 'TYN_KUL_RT_Y_T_60'
    cursor = client.flight.historyLowPrice_flightLine.find({'_id': queryId})
    if cursor.count() > 0:
        doc = cursor.next()
        sample = dict(doc)
        del sample['_id']
        del sample['fn']
        print(sample)
        start = time.time()
        df = pd.read_csv(createStringIO(sample))
        print(df)
        capAndFloor = getCapAndFloor(df)
        print('capAndFloor=' + str(capAndFloor))
        print("cap = %s" % capAndFloor[0])
        df['cap'] = capAndFloor[0]
        df['floor'] = capAndFloor[1]
        print(df.tail(n=5))  # 默认打印df的末尾5个
        # 增长趋势的模型参数:
        # - growth:增长趋势模型。整个预测模型的核心组件，分为两种：”linear”与”logistic”，分别代表线性与非线性的增长，默认值：”linear”。
        # - changepoints: 指定潜在改变点，如果不指定，将会自动选择潜在改变点例如：changepoints=['2014-01-01']指定2014-01-01这一天是潜在的changepoints
        # - n_changepoints:默认值为25，表示changepoints的数量大小，如果changepoints指定，该传入参数将不会被使用。如果changepoints不指定，将会从输入的历史数据前80%中选取25个（个数由n_changepoints传入参数决定）潜在改变点。
        # - yearly_seasonality:指定是否分析数据的年季节性，如果为True,最后会输出，yearly_trend,yearly_upper,yearly_lower等数据。
        # - weekly_seasonality:指定是否分析数据的周季节性，如果为True，最后会输出，weekly_trend,weekly_upper,weekly_lower等数据
        # - holidays:传入pd.dataframe格式的数据。这个数据包含有holiday列 (string)和ds(date类型）和可选列lower_window和upper_window来指定该日期的lower_window或者upper_window范围内都被列为假期。lower_window=-2将包括前2天的日期作为假期
        # - seasonality_prior_scale：季节性模型的调节强度，较大的值允许模型以适应更大的季节性波动，较小的值抑制季节性。
        # - holidays_prior_scale:假期组件模型的调节强度。
        # - changepoints_prior_scale:增长趋势模型的灵活度。自动的潜在改变点的灵活性调节参数，较大值将允许更多的潜在改变点，较小值将允许更少的潜在改变点。
        #       调节”changepoint”选择的灵活度，值越大，选择的”changepoint”越多，从而使模型对历史数据的拟合程度变强，然而也增加了过拟合的风险。默认值：0.05。
        # - mcmc_samples:整数，若大于0，将做mcmc样本的全贝叶斯推理，如果为0，将做最大后验估计。指定贝叶斯抽样，例如mcmc_samples=20，
        # - interval_width:浮点数，给预测提供不确定性区间宽度，如果mcmc_samples=0,这将是预测的唯一不确定性，如果mcmc_samples>0，这将会被集成在所有的模型参数中，其中包括季节性不确定性
        # - uncertainty_samples:模拟绘制数，用于估计不确定的时间间隔
        m = Prophet(growth='logistic', changepoint_prior_scale=0.01, yearly_seasonality=True, weekly_seasonality=True)
        m.fit(df)
        print('fit:' + str((time.time() - start)))
        future = m.make_future_dataframe(periods=365)
        future['cap'] = capAndFloor[0]
        future['floor'] = capAndFloor[1]
        forecast = m.predict(future)
        print('predict:' + str((time.time() - start)))
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        print(m.plot(forecast))
        m.plot(forecast).show()
        # m.plot_components(forecast).show()
    else:
        print("query flight line [%s] data count is %d" % (queryId, cursor.count()))
