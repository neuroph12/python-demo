#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : classify_demo.py
# @Author: wu gang
# @Date  : 2018/9/4
# @Desc  : 在一个模拟数据集上训练神经网络来解决二分类问题
# @Contact: 752820344@qq.com

import tensorflow as tf
from numpy.random import RandomState

# 训练神经网络的三个步骤：
# 1、定义神经网络的结构和前向传播的输出结果；
# 2、定义损失函数以及选择反向传播优化的算法；
# 3、生成会话(tf.Session)并且在训练数据上反复运行反向传播优化算法；

if __name__ == '__main__':
    # 1. 定义神经网络的参数，输入和输出节点。
    batch_size = 8  # 定义训练数据集的batch大小
    # 定义神经网络的参数
    # 声明w1和w2两个变量。通过seed参数设置随机种子，可以保证每次运行得到的结果一样
    w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
    w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))

    # 只提供一个batch的情况：每次选出的的一小部分数据叫做batch
    # 暂时将输入的特征向量定义为一个常量，X为1*2的矩阵
    # x = tf.constant([[0.7, 0.9]])
    # 定义placeholder来存放输入数据，(如纬度确定，可以直接定义，降低出错的概率)
    # x = tf.placeholder(tf.float32, shape=(1, 2), name="input")

    # 提供多个batch：3个batch，输入x为3*2的矩阵，输出计算结果y为3*1的矩阵
    # x = tf.placeholder(tf.float32, shape=(3, 2), name="input")

    # 在shape的一个维度上使用None可以方便使用不同的batch大小；
    # 在训练时，需要把数据分成比较小的batch；测试时可以全部一次性使用；
    # 当数据集比较大时，一次性使用容易造成内存溢出。
    x = tf.placeholder(tf.float32, shape=(None, 2), name="x-input")
    y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')

    # 2. 定义前向传播过程，损失函数及反向传播算法。
    # 定义神经网络的前向传播过程
    # tf.matmul(): 矩阵乘法函数
    a = tf.matmul(x, w1)  # 隐藏层
    y = tf.matmul(a, w2)  # 输出层

    # 在得到batch的前向传播结果后，需要定义一个损失函数来描述当前的预测值和真实答案之间的差距
    # 然后通过"反向传播算法"来调整神经网络中参数的取值，使两者差距不断缩小。
    # 使用sigmoid函数将y转为[0-1]之间的数值。
    # 转换后"y"代表预测是正样本的概率；"1-y"代表预测是负样本的概率
    # 定义损失函数和反向传播的算法
    y = tf.sigmoid(y)
    # 定义损失函数来描述当前的预测值和真实答案之间的差距
    # cross_entropy定义了真实值和预测值之间的交叉熵
    cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0))
                                    + (1 - y_) * tf.log(tf.clip_by_value(1 - y, 1e-10, 1.0)))
    # 定义学习率
    learning_rate = 0.001
    # 定义反向传播算法来优化神经网络中的参数
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
    # 3. 生成模拟数据集。
    # 通过随机数生成一个模拟数据集
    rdm = RandomState(1)
    X = rdm.rand(128, 2)
    # 定义规则来给出样本的标签。
    # "x1 + x2 < 1"为正样本，其他为负样本。
    Y = [[int(x1 + x2 < 1)] for (x1, x2) in X]
    # 4. 创建一个会话来运行TensorFlow程序。
    with tf.Session() as sess:
        # 这里不能直接通过sess.run(y)来获取y的取值。
        # 因为w1和w2都还没运行初始化过程。
        # 逐个初始化变量
        # sess.run(w1.initializer) # 初始化w1
        # sess.run(w2.initializer)
        # tf.global_variables_initializer()函数初始化所有变量,也会自动处理变量直接的依赖关系
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        # 输出目前（未经训练）的参数取值。
        print("输出目前（未经训练）的参数取值：")
        print(sess.run(w1))
        print(sess.run(w2))
        print("\n")

        # 训练模型。
        STEPS = 5000  # 训练的轮数
        for i in range(STEPS):
            # 每次选batch_size个样本进行训练
            start = (i * batch_size) % 128
            end = (i * batch_size) % 128 + batch_size
            # 通过选取的样本训练神经网络并更新参数
            # 对所有在GraphKeys.TRAINABLE_VARIABLES集合(存放需要优化的参数变量)中的变量进行优化，使得在当前batch下损失函数最小
            sess.run([train_step, y, y_], feed_dict={x: X[start:end], y_: Y[start:end]})
            if i % 1000 == 0:
                # 每隔一段时间计算所在数据上的交叉熵并输出
                total_cross_entropy = sess.run(cross_entropy, feed_dict={x: X, y_: Y})
                # 交叉熵是逐渐变小的，说明预测的结果与真实结果差距越来越小
                print("After %d training step(s), cross entropy on all data is %g" % (i, total_cross_entropy))

        # 输出训练后的参数取值。
        print("\n")
        print("输出训练后的参数取值：")
        print(sess.run(w1))
        print(sess.run(w2))
