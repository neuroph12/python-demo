#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : img_compress.py
# @Author: wu gang
# @Date  : 2018/10/11
# @Desc  : 利用SVD图像压缩:原始的图像大小是32×32=1024像素
# @Contact: 752820344@qq.com

import numpy as np
from numpy import linalg as la


def loadData():
    """
    加载数据
    """
    data = []
    for line in open('0.txt').readlines():
        row = []
        for i in range(32):
            row.append(int(line[i]))
        data.append(row)
    return data


def printMat(inMat, thresh=0.8):
    """
    打印矩阵:
    由于矩阵包含了浮点数，因此必须定义浅色和深色。
    这里通过一个阈值来界定，后面也可以调节该值。
    该函数遍历所有的矩阵元素，当元素大于阈值时打印1，否则打印0。
    :param inMat: 矩阵
    :param thresh: 阈值
    """
    for i in range(32):
        for k in range(32):
            if float(inMat[i, k]) > thresh:
                print(1, sep='', end='')
            else:
                print(0, sep='', end='')
        print('', sep='', end='\n')


def imgCompress(numSV=3, thresh=0.8):
    """
    允许基于任意给定的奇异值数目来重构图像:
    步骤：
        该函数构建 了一个列表，然后打开文本文件，并从文件中以数值方式读入字符。
        对原始图像进行SVD分解并重构图像；
        通过将Sigma重新构成SigRecon来实现这一点。Sigma是一个对角矩阵，因此需要建立一个全0矩阵，
        然后将前面的那些奇异值填充到对角线上。
        最后，通过截断的U和VT矩阵，用SigRecon得到重构后的矩阵；
        该矩阵通过printMat()函数输出。
    :param numSV: 奇异值数目
    :param thresh: 阈值
    :return:
    """
    myl = loadData()
    myMat = np.mat(myl)
    print("****original matrix******")
    printMat(myMat, thresh)

    U, Sigma, VT = la.svd(myMat)
    # 初始化元素都为0的对角矩阵
    SigRecon = np.mat(np.zeros((numSV, numSV)))
    # 利用Sigma向量构造对角矩阵
    for k in range(numSV):
        SigRecon[k, k] = Sigma[k]
    # U[:, :numSV]取出每行的第0到numSV列元素
    # SigRecon 前numSV个奇异值
    # VT[:numSV, :] 取出0到numSV行到每一列元素
    # 根据SVD公式可知，三者相乘就可以得到原始矩阵
    print("svd取前%d个元素后的U：\n %s" % (numSV, U[:, :numSV]))
    print("svd取前%d个Sigma奇异值后的对角矩阵：\n %s" % (numSV, SigRecon))
    print("svd取前%d个元素后的VT：\n %s" % (numSV, VT[:numSV, :]))
    reconMat = U[:, :numSV] * SigRecon * VT[:numSV, :]
    print("****reconstructed matrix using %d singular values******" % numSV)
    printMat(reconMat, thresh)


def choseNumSVD(mat, num=3):
    # 计算该矩阵的SVD来了解其到底需要多少维特征,有多少个奇异值能达到总能量的80%-90%.
    U, Sigma, VT = la.svd(mat)
    # 对Sigma中的值求平方
    sig2 = Sigma ** 2
    # 计算一下总能量
    total = sum(sig2)
    print("总能量：%.2f" % total)
    # 计算总能量的90%:
    thresholdEnergy = total * 0.9
    print("总能量的80%%~90%%: %.2f ~ %.2f" % (total * 0.8, thresholdEnergy))
    # 计算前3个元素所包含的能量:
    eg = sum(sig2[:num])
    print("计算前%d个元素所包含的能量: %.2f" % (num, eg))
    print("前%d个元素所包含的能量占总能量的: %.2f%%" % (num, eg / total * 100))


if __name__ == '__main__':
    myl = loadData()
    myMat = np.mat(myl)
    choseNumSVD(myMat, num=2)

    # U和VT都是32×2的矩阵，有两个奇异值。
    # 因此总数字数目是 64+64+2=130。和原数目1024相比，我们获得了几乎10倍的压缩比。
    imgCompress(2)
