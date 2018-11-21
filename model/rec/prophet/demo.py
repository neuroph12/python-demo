#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : demo.py
# @Author: wu gang
# @Date  : 2018/10/26
# @Desc  : 
# @Contact: 752820344@qq.com

import matplotlib

matplotlib.use('Agg')
import time
import json
import pandas as pd
from io import *
from fbprophet import Prophet
import sys
from pymongo import MongoClient

client = MongoClient("120.133.0.172:27017", authSource="flight", username='search', password='search@huoli123',
                     authMechanism='MONGODB-CR')


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
        maxy = df.loc[df['y'] != None, 'y'].max()
        print("maxy=" + str(maxy))
        # 碰到特殊数据，每天的价格相差不大，数据条数很少，这种情况会把所有数据都置为none，故先注释
        # if df.iloc[:,0].size < 10:
        #     break
        # if maxy>0 and len(df.loc[df['y']>=(maxy*0.8),'y'])<10:
        #      df.loc[df['y']==maxy,'y']=None
        # else:
        #      break
        break
    while True:
        miny = df.loc[df['y'] != None, 'y'].min()
        print("miny=" + str(miny))
        # if df.iloc[:,0].size < 10:
        #     break
        # if miny>0 and len(df.loc[df['y']<=(miny*1.2),'y'])<10:
        #     df.loc[df['y']==miny,'y']=None
        # else:
        #     break
        break
    capAndFloor = [df.loc[df['y'] != None, 'y'].max(), df.loc[df['y'] != None, 'y'].min()]
    return capAndFloor


if __name__ == '__main__':
    testdict = json.loads(
        "{\"2018-07-06\": \"200\", \"2018-07-07\": \"5770\", \"2018-07-08\": \"5770\", \"2018-07-09\": \"5770\", \"2018-07-10\": \"5771\", \"2018-07-11\": \"5770\", \"2018-07-12\": \"5814\"}")
    df = pd.read_csv(createStringIO(testdict))
    print(df)
    capAndFloor = getCapAndFloor(df)
    print('capAndFloor=' + str(capAndFloor))
    df['cap'] = capAndFloor[0]
    df['floor'] = capAndFloor[1]
    print(df.tail())


def getPriceTrendGraph(sample):
    # queryId='BKK_FOC_RT_Y_D'
    # cursor = client.flight.historyLowPrice_flightLine.find({'_id':queryId})
    # if(cursor.count()>0):
    #     doc=cursor.next();
    #     sample=dict(doc)
    #     del sample['_id']
    #     del sample['fn']
    # print(sample)
    start = time.time()
    df = pd.read_csv(createStringIO(sample))
    print(df)
    capAndFloor = getCapAndFloor(df)
    print('capAndFloor=' + str(capAndFloor))
    df['cap'] = capAndFloor[0]
    df['floor'] = capAndFloor[1]
    print(df.tail())
    m = Prophet(changepoint_prior_scale=0.01, growth='logistic', yearly_seasonality=True, weekly_seasonality=True)
    m.fit(df)
    print('fit:' + str((time.time() - start)))
    future = m.make_future_dataframe(periods=365)
    future['cap'] = capAndFloor[0]
    future['floor'] = capAndFloor[1]
    forecast = m.predict(future)
    print('predict:' + str((time.time() - start)))
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
    print(m.plot(forecast))
    forecast.index.name = None
    # return forecast.loc[:,['ds','yhat']]
    return forecast.loc[:, ['ds', 'yhat']].to_json()
    # m.plot(forecast)
    # m.plot_components(forecast).show()
    # plt.show()


def getFlightLineHistoryPrice(queryId):
    cursor = client.flight.historyLowPrice_flightLine.find({'_id': queryId})
    if (cursor.count() > 0):
        doc = cursor.next();
        sample = dict(doc)
        del sample['_id']

        if 'fn' in sample:
            del sample['fn']
        print('sample:' + str(sample))
        return sample
