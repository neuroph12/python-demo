#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : predict.py
# @Author: wu gang
# @Date  : 2018/10/19
# @Desc  : 簡單的基於tensorflow seq2seq字符串訓練，實現人機對話。
# @Contact: 752820344@qq.com

import tensorflow as tf

import numpy as np

import jieba

filepath = "/media/hadoop/disk/rpn2/cn.txt"
file = open(filepath)
filename = []
word_to_id = {}
max_len = 0
dic = []
dic_to_id = {}
sentence_list = []
dic.append("PADID")  # 補0
dic.append("BID")  # 開始
dic.append("EID")  # 結束

for line in file:

    seg_list = jieba.cut(line.strip())

    # print(" ".join(seg_list))
    sentence = " ".join(seg_list)
    word = sentence.split(" ")
    print(word)
    for w in word:
        if w not in dic:
            dic.append(w)
    sentence_list.append(word)
# print(dic)
num = 0
for w in dic:
    word_to_id[w] = num
    num = num + 1
# print("word_to_id:",word_to_id)
# print(sentence_list)
sentence_to_id = []
for s in sentence_list:
    sent = []
    sent.append(word_to_id["BID"])
    for wd in s:
        sent.append(word_to_id[wd])
    sent.append(word_to_id["EID"])
    sentence_to_id.append(sent)

for key in word_to_id:
    dic_to_id[word_to_id[key]] = key

learning_rate = 0.1

length = 15
batch_size = 1
encoder_inputs = tf.placeholder(dtype=tf.int32, shape=[length, batch_size])
decoder_inputs = tf.placeholder(dtype=tf.int32, shape=[length, batch_size])

# logits=tf.placeholder(dtype=tf.float32,shape=[10])
targets = tf.placeholder(dtype=tf.int32, shape=[length, batch_size])
weights = tf.placeholder(dtype=tf.float32, shape=[length, batch_size])

train_e_in = []
train_d_in = []
train_w = np.ones(shape=[length, batch_size], dtype=np.float32)

num_encoder_symbols = len(dic)
num_decoder_symbols = len(dic)
embedding_size = 5
cell = tf.nn.rnn_cell.BasicLSTMCell(5)

# 补零
count = 0
for sent in sentence_to_id:
    print(len(sent))
    d = length - len(sent)
    # s = (1,d)
    sent2 = []
    if d > 0:
        for s in sent:
            sent2.append(s)
        for i in range(d):
            sent2.append(0)
    else:
        sent2 = sent
    print(sent2)
    if count % 2 == 0:
        train_e_in.append(sent2)
    else:
        train_d_in.append(sent2)
    count = count + 1

print("train_e_in:", train_e_in)


# print("train_d_in:",train_d_in.shape)

def seq2seq(encoder_inputs, decoder_inputs, cell, num_encoder_symbols, num_decoder_symbols, embedding_size):
    encoder_inputs = tf.unstack(encoder_inputs, axis=0)
    decoder_inputs = tf.unstack(decoder_inputs, axis=0)
    results, states = tf.contrib.legacy_seq2seq.embedding_rnn_seq2seq(
        encoder_inputs,
        decoder_inputs,
        cell,
        num_encoder_symbols,
        num_decoder_symbols,
        embedding_size,
        output_projection=None,
        feed_previous=False,
        dtype=None,
        scope=None
    )
    return results


def get_loss(logits, targets, weights):
    loss = tf.contrib.seq2seq.sequence_loss(
        logits,
        targets=targets,
        weights=weights
    )
    return loss


results = seq2seq(encoder_inputs, decoder_inputs, cell, num_encoder_symbols, num_decoder_symbols, embedding_size)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
saver = tf.train.import_meta_graph('Model/model.ckpt-240.meta')
saver.restore(sess, tf.train.latest_checkpoint('Model/'))

for i in range(1000):
    input_seq = input('请输入：')

    seq_list2 = jieba.cut(input_seq.strip())

    sentence = " ".join(seq_list2)
    word = sentence.split(" ")
    s_to_id = []
    s_to_id.append(word_to_id["BID"])

    for w in word:
        print(w)
        s_to_id.append(word_to_id[w])
    print(s_to_id)
    s_to_id.append(word_to_id["EID"])
    d = length - len(s_to_id)
    if d > 0:
        for di in range(d):
            s_to_id.append(0)
    print(s_to_id)
    train_d = sess.run(tf.expand_dims(s_to_id, -1))
    train_e = sess.run(tf.expand_dims(train_e_in[0], -1))
    results_value = sess.run(results, feed_dict={encoder_inputs: train_e, decoder_inputs: train_d})
    outputs_seq = [int(np.argmax(logit[0], axis=0)) for logit in results_value]
    print(outputs_seq)
    cn = []
    for o in outputs_seq:
        word = dic_to_id[o]
        cn.append(word)
        print("回復:", cn)