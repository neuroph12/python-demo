#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test01.py
# @Author: wu gang
# @Date  : 2018/8/28
# @Desc  : 
# @Contact: 752820344@qq.com

import os
import tensorflow as tf

# os.environ["TF_CPP_MIN_LOG_LEVEL"] = '1'  # 这是默认的显示等级，显示所有信息
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'  # 只显示 warning 和 Error


# os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'  # 只显示 Error

# 1. 定义两个不同的图
#  两个阶段：定义图中的所有计算；执行计算
def define_graph():
    g1 = tf.Graph()
    with g1.as_default():
        # 计算图g1中定义变量v，并设置初始值为0
        v = tf.get_variable("v", shape=[1], initializer=tf.zeros_initializer)

    g2 = tf.Graph()
    with g2.as_default():
        # 计算图g2中定义变量v，并设置初始值为1
        v = tf.get_variable("v", shape=[1], initializer=tf.ones_initializer)

    # 在计算图g1中读取变量v的取值
    with tf.Session(graph=g1) as sess:
        tf.global_variables_initializer().run()
        with tf.variable_scope("", reuse=True):
            # 在计算图g1中，v的取值为0，所以下面会输出[0.]
            print(sess.run(tf.get_variable("v")))

    with tf.Session(graph=g2) as sess:
        tf.global_variables_initializer().run()
        with tf.variable_scope("", reuse=True):
            # 在计算图g2中，v的取值为1，所以下面会输出[1.]
            print(sess.run(tf.get_variable("v")))


# tf.Graph().device函数指定运行计算的设备：gpu/cpu
def gpu():
    g = tf.Graph()
    # 指定计算运行的设备
    with g.device('/gpu:0'):
        print("execute by gpu 0")


if __name__ == '__main__':
    define_graph()



