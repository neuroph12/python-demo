#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : forward_propagation_demo.py
# @Author: wu gang
# @Date  : 2018/9/4
# @Desc  : 前向传播示例
# @Contact: 752820344@qq.com

import tensorflow as tf

if __name__ == '__main__':
    # 声明w1和w2两个变量。通过seed参数设置随机种子，可以保证每次运行得到的结果一样
    w1 = tf.Variable(tf.random_normal((2, 3), stddev=1, seed=1))
    w2 = tf.Variable(tf.random_normal((3, 1), stddev=1, seed=1))

    # 只提供一个batch的情况：每次选出的的一小部分数据叫做batch
    # 暂时将输入的特征向量定义为一个常量，X为1*2的矩阵
    # x = tf.constant([[0.7, 0.9]])
    # 定义placeholder来存放输入数据，(如纬度确定，可以直接定义，降低出错的概率)
    # x = tf.placeholder(tf.float32, shape=(1, 2), name="input")

    # 提供多个batch：3个batch，输入x为3*2的矩阵，输出计算结果y为3*1的矩阵
    x = tf.placeholder(tf.float32, shape=(3, 2), name="input")

    # tf.matmul():矩阵乘法函数
    # 实现前向传播算法获得神经网络的输出
    a = tf.matmul(x, w1)  # 隐藏层
    y = tf.matmul(a, w2)  # 输出层

    with tf.Session() as sess:
        # 这里不能直接通过sess.run(y)来获取y的取值。
        # 因为w1和w2都还没运行初始化过程。
        # 逐个初始化变量
        # sess.run(w1.initializer) # 初始化w1
        # sess.run(w2.initializer)
        # tf.global_variables_initializer()函数初始化所有变量,也会自动处理变量直接的依赖关系
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        # 输出y
        # result = sess.run(y)
        # 输出y，用feed_dict来指定x的取值
        # y = sess.run(y, feed_dict={x: [[0.7, 0.9]]})
        # print(y)
        # 因为x定义时定义了3个batch，所以在前向传播的过程中需提供3个样例数据
        y_batch3 = sess.run(y, feed_dict={x: [[0.7, 0.9], [0.1, 0.4], [0.5, 0.8]]})
        print(y_batch3)

        # 在得到batch的前向传播结果后，需要定义一个损失函数来描述当前的预测值和真实答案之间的差距
        # 然后通过"反向传播算法"来调整神经网络中参数的取值，使两者差距不断缩小。
        # 使用sigmoid函数将y转为[0-1]之间的数值。
        # 转换后"y"代表预测是正样本的概率；"1-y"代表预测是负样本的概率
        y_batch3 = tf.sigmoid(y_batch3)
        # 定义损失函数来描述当前的预测值和真实答案之间的差距
        # cross_entropy定义了真实值和预测值之间的交叉熵
        cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0))
                                        + (1 - y_) * tf.log(tf.clip_by_value(1 - y, 1e-10, 1.0)))
        # 定义学习率
        learning_rate = 0.001
        # 定义反向传播算法来优化神经网络中的参数
        train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
        # 对所有在GraphKeys.TRAINABLE_VARIABLES集合(存放需要优化的参数变量)中的变量进行优化，使得在当前batch下损失函数最小
        sess.run(train_step)
