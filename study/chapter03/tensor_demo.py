#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : tensor_demo.py
# @Author: wu gang
# @Date  : 2018/9/3
# @Desc  : 张量：tf中所有数据都是通过tensor的形式来组织的
# @Contact: 752820344@qq.com

import tensorflow as tf

if __name__ == '__main__':
    a = tf.constant([1.0, 2.0], name="a")
    b = tf.constant([2.0, 3.0], name="b")
    result = tf.add(a, b, name="add")
    print(result)
    # 输出的张量并没有保存真正的数字，而是如何得到这些数字的计算过程：
    # 输出： Tensor("add:0", shape=(2,), dtype=float32)
    r = a + b
    print(r)
    # 通过Session会话获取张量Tensor计算的结果
    sess = tf.Session()  # 创建一个会话
    addValue = sess.run(result)
    print(addValue)
    sess.close()  # 关闭会话，释放资源

    # 通过python的上下文管理器管理这个会话
    # 不需要显示的去调用close函数，当上下文退出时会话会关闭，资源会释放
    with tf.Session() as sess:
        addValue = sess.run(result)
        print(addValue)
        # 使用tf.Tensor.eval()函数计算一个张量的取值
        print(result.eval())

    # 神经网络参数与TensorFlow变量
    # 变量Variable：保存和更新神经网络中的参数
    # 初始化一个2*3但矩阵，元素均值为0，标准差为2的随机数
    weights = tf.Variable(tf.random_normal([2, 3], stddev=2))
    print(weights)
    # w2与weights变量相同
    w2 = tf.Variable(weights.initialized_value())
    # w3初始值是weights变量的2倍
    w3 = tf.Variable(weights.initialized_value() * 2.0)

    # 偏置项bias：通常用常数设置初始值
    # 初始值全为0且长度为3的变量
    biases = tf.Variable(tf.zeros([3]))



