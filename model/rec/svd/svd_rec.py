#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : svd_rec.py
# @Author: wu gang
# @Date  : 2018/10/11
# @Desc  : 基于SVD的推荐demo
# @Contact: 752820344@qq.com

import numpy as np
from numpy import linalg as la


def loadData():
    return [[0, 0, 0, 2, 2],
            [0, 0, 0, 3, 3],
            [0, 0, 0, 1, 1],
            [1, 1, 1, 0, 0],
            [2, 2, 2, 0, 0],
            [5, 5, 5, 0, 0],
            [1, 1, 1, 0, 0]]


def ecludSim(inA, inB):
    """
    欧氏距离:
        相似度=1/(1+距离)
        相似度值在0到1之间变化，并且物品对越相似，它们的 相似度值也就越大.
    """
    # 范数的计算方法linalg.norm()
    distance = la.norm(inA - inB)
    # print("默认参数(矩阵2范数，不保留矩阵二维特性)：", distance)
    return 1.0 / (1.0 + distance)


def pearsSim(inA, inB):
    """
    皮尔逊相关系数：
    在NumPy中， 皮尔逊相关系数的计算是由函数corrcoef()进行的；
    皮尔逊相关 系数的取值范围从-1到+1，我们通过0.5 + 0.5*corrcoef()这个函数计算，并且把其取值范 围归一化到0到1之间。
    """
    if len(inA) < 3:
        return 1.0
    return 0.5 + 0.5 * np.corrcoef(inA, inB, rowvar=0)[0][1]


def cosSim(inA, inB):
    """
    余弦相似度：
    计算的是两个向量夹角的 余弦值。如果夹角为90度，则相似度为0;如果两个向量的方向相同，则相似度为1.0。
    余弦相似度的取值范围也在-1到+1之间，也将它归一化到0到1之间。
    """
    num = float(inA.T * inB)
    denom = la.norm(inA) * la.norm(inB)
    return 0.5 + 0.5 * (num / denom)


def standEst(dataMat, user, item, simMeas):
    """
    基于物品相似度的推荐引擎
    :param dataMat: 数据矩阵 m*n矩阵，一般m为用户，n为物品。
    :param user: 用户编号
    :param item: 物品编号
    :param simMeas: 相似度计算方法
    :return: 预测评分
    """
    n = np.shape(dataMat)[1]  # 数据集中的物品数目
    simTotal = 0.0
    ratSimTotal = 0.0
    for j in range(n):
        userRating = dataMat[user, j]  # 物品评分值
        # 某个物品评分值为0，就意味着用户没有对该物品评分，跳过了这个物品
        if userRating == 0:
            continue
        # 逻辑与
        logicalAnd = np.logical_and(dataMat[:, item].A > 0, dataMat[:, j].A > 0)
        # 两个物品当中已经被评分的那个元素
        overLap = np.nonzero(logicalAnd)[0]
        # 如果两者没有任何重合元素，则相似度为0且 中止本次循环。
        # 如果存在重合的物品，则基于这些重合物品计算相似度
        if len(overLap) == 0:
            similarity = 0
        else:
            similarity = simMeas(dataMat[overLap, item], dataMat[overLap, j])
        print('the %d and %d similarity is: %f' % (item, j, similarity))
        # 相似度会不断累加，每次计算时还考虑相似度和当前用户评分的乘积。
        simTotal += similarity
        ratSimTotal += similarity * userRating
    # 最后，通过除以所有的评分总和，对 上述相似度评分的乘积进行归一化。
    # 这就可以使得最后的评分值在0到5之间(因为评分区间在0-5)，而这些评分值则用 于对预测值进行排序。
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal


def svdEst(dataMat, user, item, simMeas, numSV=4):
    """
    基于SVD的推荐引擎
    :param dataMat: 数据矩阵 m*n矩阵，一般m为用户，n为物品。
    :param user: 用户编号
    :param item: 物品编号
    :param simMeas: 相似度计算方法
    :param numSV: 奇异值个数，默认4
    :return: 预测评分
    """
    n = np.shape(dataMat)[1]  # 数据集中的物品数目
    simTotal = 0.0
    ratSimTotal = 0.0
    # 任意一个M*N的矩阵A（M行*N列，M>N），可以被写成三个矩阵的乘积：
    # U：（M行M列的列正交矩阵）
    # Sigma：（M*N的对角线矩阵，矩阵元素非负）
    # VT：（N*N的正交矩阵的倒置）
    U, Sigma, VT = la.svd(dataMat)
    # np.eye(4)建立4*4对角矩阵
    Sig = np.mat(np.eye(numSV) * Sigma[:numSV])
    # SVD构建转换后的物品
    # dataMat.T 矩阵转置
    # U[:, :numSV]取出每行的第0到numSV列元素，也就是每个用户评价过的所有物品（一般情况下，行为用户，列为物品）
    # Sig4.I 矩阵求逆
    xformedItems = dataMat.T * U[:, :numSV] * Sig.I
    for j in range(n):
        userRating = dataMat[user, j]
        # 某个物品评分值为0，就意味着用户没有对该物品评分，或者j == item（不去计算两个相同物品的相似度），跳过了这个物品
        if userRating == 0 or j == item:
            continue
        # xformedItems[item, :].T 映射后的矩阵中item行的全部列元素，之后矩阵转置，变成xxx坐标向量样式，如(x, y, z...)
        # xformedItems[j, :].T 映射后的矩阵中j行的全部列元素，之后矩阵转置，变成xxx坐标向量样式，如(x, y, z...)
        similarity = simMeas(xformedItems[item, :].T, xformedItems[j, :].T)
        print('the %d and %d similarity is: %f' % (item, j, similarity))
        # 相似度会不断累加，每次计算时还考虑相似度和当前用户评分的乘积。
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal


def recommend(dataMat, user, N=3, simMeas=cosSim, estMethod=standEst):
    """
    推荐功能
    :param dataMat: 数据矩阵
    :param user: 用户编号
    :param N: 推荐结果数量
    :param simMeas: 相似度计算方法
    :param estMethod: 估计(推荐)方法
    :return: 推荐结果
    步骤：
        (1)寻找用户没有评级的物品，即在用户-物品矩阵中的0值;
        (2)在用户没有评级的所有物品中，对每个物品预计一个可能的评级分数。这就是说，我们认为用户可能会对物品的打分(这就是相似度计算的初衷);
        (3)对这些物品的评分从高到低进行排序，返回前N个物品。
    """
    # print('type', dataMat[:,:4]) #the number user line or col
    print(np.nonzero(dataMat[user, :].A == 0))  # to array
    # 对给定的用户建立一个未评分的物品列表
    unRatedItems = np.nonzero(dataMat[user, :].A == 0)[1]
    print("unRatedItems: \n", unRatedItems)
    # unratedItems = np.nonzero(dataMat[user,:].A==0)[1] #find unrated items
    # 如果不存在未评分物品，那么就退出函数;否则，在所有的未评分物品上进行循环
    if len(unRatedItems) == 0:
        return 'you rated everything'
    itemScores = []
    for item in unRatedItems:
        # 对每个未评分物品，则通过调用 standEst()来产生该物品的预测得分
        estimatedScore = estMethod(dataMat, user, item, simMeas)
        # 该物品的编号和估计得分值会放在一个元素列表itemScores中。
        itemScores.append((item, estimatedScore))
    # 最后按照估计得分，对该列表进行从大到小逆序排列并返回
    return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]


def loadRecData():
    return [[4, 4, 0, 2, 2],
            [4, 0, 0, 3, 3],
            [4, 0, 0, 1, 1],
            [1, 1, 1, 2, 0],
            [2, 2, 2, 0, 0],
            [1, 1, 1, 0, 0],
            [5, 5, 5, 0, 0]]


def loadRecSVDData():
    return [[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
            [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
            [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
            [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
            [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
            [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
            [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
            [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]


def run():
    # data = loadData()
    # U, Sigma, VT = la.svd(data)
    # print("U: \n", U)
    # print("Sigma: \n", Sigma)
    # print("VT: \n", VT)
    #
    # myMat = np.mat(data)
    # ecludsim = ecludSim(myMat[:, 0], myMat[:, 4])
    # print("sim = ", ecludsim)

    # # 计算该矩阵的SVD来了解其到底需要多少维特征,有多少个奇异值能达到总能量的90%.
    # U, Sigma, VT = la.svd(loadRecSVDData())
    # # 对Sigma中的值求平方
    # sig2 = Sigma ** 2
    # # 计算一下总能量
    # total = sum(sig2)
    # # 计算总能量的90%:
    # thresholdEnergy = total * 0.9
    # print(thresholdEnergy)
    # # 计算前3个元素所包含的能量:
    # eg = sum(sig2[:3])
    # print(eg)

    recSVDMat = np.mat(loadRecSVDData())
    svdRecItems = recommend(recSVDMat, 2, 3, ecludSim, estMethod=svdEst)
    print("svd rec: \n", svdRecItems)

    recMat = np.mat(loadRecData())
    standRecItems = recommend(recMat, 2, 3, ecludSim, standEst)
    svdRecItems2 = recommend(recMat, 2, 3, ecludSim, estMethod=svdEst)
    print("stand rec: \n", standRecItems)
    print("svd rec: \n", svdRecItems2)


if __name__ == '__main__':
    run()
