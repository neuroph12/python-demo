#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : prediction.py
# @Author: wu gang
# @Date  : 2018/10/25
# @Desc  : 预测天朝铁路客运量。参考：http://blog.topspeedsnail.com/archives/10845
# @Contact: 752820344@qq.com

import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import tensorflow as tf
from pymongo import MongoClient


def createStringIO(priceMap):
    valueIO = io.StringIO()
    valueIO.write('ds,y\n')
    entries = list(priceMap.items())
    entries.sort()
    for ds, y in entries:
        valueIO.write(ds + ',' + str(y) + '\n')
    return io.StringIO(valueIO.getvalue())


def load_mongo():
    client = MongoClient("120.133.0.172:27017", authSource="flight", username='search', password='search@huoli123',
                         authMechanism='MONGODB-CR')
    queryId = 'BJS_LAX_RT_Y_D_10-01'
    cursor = client.flight.historyLowPrice_flightLine.find({'_id': queryId})
    if (cursor.count() > 0):
        doc = cursor.next()
        sample = dict(doc)
        del sample['_id']
        del sample['fn']
    print(sample)
    df = pd.read_csv(createStringIO(sample))  # python2使用StringIO.StringIO
    return df


def testMongo():
    df = load_mongo()
    time = np.array(df['ds'])
    data = np.array(df['y'])
    # 使用figure()函数重新申请一个figure对象
    # 注意，每次调用figure的时候都会重新申请一个figure对象
    plt.figure()
    # 第一个是横坐标的值，第二个是纵坐标的值
    plt.plot(time, data)
    plt.show()


def load_csv(file_name):
    df = pd.read_csv(file_name)
    return df


def load_from_net(url_file):
    ass_data = requests.get(url_file).content
    df = pd.read_csv(io.StringIO(ass_data.decode('utf-8')))  # python2使用StringIO.StringIO
    return df


# regression
def ass_rnn(hidden_layer_size=6):
    W = tf.Variable(tf.random_normal([hidden_layer_size, 1]), name='W')
    b = tf.Variable(tf.random_normal([1]), name='b')
    cell = tf.nn.rnn_cell.BasicLSTMCell(hidden_layer_size)
    outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
    W_repeated = tf.tile(tf.expand_dims(W, 0), [tf.shape(X)[0], 1, 1])
    # out = tf.batch_matmul(outputs, W_repeated) + b
    out = tf.matmul(outputs, W_repeated) + b
    out = tf.squeeze(out)
    return out


def train_rnn():
    out = ass_rnn()

    loss = tf.reduce_mean(tf.square(out - Y))
    train_op = tf.train.AdamOptimizer(learning_rate=0.003).minimize(loss)

    saver = tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        # tf.get_variable_scope().reuse_variables()
        sess.run(tf.global_variables_initializer())

        for step in range(10000):
            _, loss_ = sess.run([train_op, loss], feed_dict={X: train_x, Y: train_y})
            if step % 10 == 0:
                # 用测试数据评估loss
                print(step, loss_)
        print("保存模型: ", saver.save(sess, './ass.model'))


def prediction():
    out = ass_rnn()

    saver = tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        # tf.get_variable_scope().reuse_variables()
        saver.restore(sess, './ass.model')

        prev_seq = train_x[-1]
        predict = []
        for i in range(12):
            next_seq = sess.run(out, feed_dict={X: [prev_seq]})
            predict.append(next_seq[-1])
            prev_seq = np.vstack((prev_seq[1:], next_seq[-1]))

        plt.figure()
        plt.plot(list(range(len(normalized_data))), normalized_data, color='b')
        plt.plot(list(range(len(normalized_data), len(normalized_data) + len(predict))), predict, color='r')
        plt.show()


if __name__ == '__main__':
    file_name = "../../data/铁路客运量.csv"
    df = load_csv(file_name)
    # 使用matplotlib画出数据走势：总体呈增长趋势, 每年又有淡季和旺季
    # url_file = 'http://blog.topspeedsnail.com/wp-content/uploads/2016/12/铁路客运量.csv'

    time = np.array(df['时间'])
    data = np.array(df['铁路客运量_当期值(万人)'])  # 取出数据的运量
    # normalize：Z-Score数据归一化
    # data减data的去平均值 除以 矩阵标准差
    normalized_data = (data - np.mean(data)) / np.std(data)

    # 使用figure()函数重新申请一个figure对象
    # 注意，每次调用figure的时候都会重新申请一个figure对象
    plt.figure()
    # 第一个是横坐标的值，第二个是纵坐标的值
    plt.plot(time, data)
    plt.show()

    seq_size = 3
    train_x, train_y = [], []
    for i in range(len(normalized_data) - seq_size - 1):
        train_x.append(np.expand_dims(normalized_data[i: i + seq_size], axis=1).tolist())
        train_y.append(normalized_data[i + 1: i + seq_size + 1].tolist())

    input_dim = 1
    X = tf.placeholder(tf.float32, [None, seq_size, input_dim])
    Y = tf.placeholder(tf.float32, [None, seq_size])
    # train
    # train_rnn()
    # prediction
    prediction()
    load_csv()
    testMongo()
