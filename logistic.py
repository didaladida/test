# -*- encoding:utf-8 -*-

import numpy as np

"""
优化目标函数的时候用的不是真正的梯度
用真正的梯度效果反而不是太好
随机梯度下降可以减少总的迭代次数
"""


class Logistic(object):

    def __init__(self):
        print 'Logistic algorithm for two class'

    def sigmoid(self, XMat):
        # 输入列向量，输出列向量
        return 1 / (1 + np.exp(-XMat))

    def batch_train(self, X, Y, alpha=0.001, MAX_ITR=500):
        """
        二分类逻辑回归
        X.shape(样本数N，特征维数含偏置M) Yshape（样本数N）
        """
        XMat = np.mat(X)
        YMat = np.mat(Y).T
        self.N, self.M = XMat.shape
        self.W = np.random.rand(self.M, 1)

        for t in range(1, MAX_ITR + 1):
            predict_Y = self.sigmoid(XMat * self.W)
            err = predict_Y - YMat
            # 梯度
            #err=np.multiply(np.multiply(predict_Y,(1-predict_Y)),predict_Y- YMat)
            print t, ':', (np.abs(err)).sum()
            self.W = self.W - alpha * XMat.T * err

        # 训练准确率
        print 'W:', self.W
        return self.W

    def stoc_train(self, X, Y, alpha=0.01, MAX_ITR=100):
        """
        二分类逻辑回归
        X.shape(样本数N，特征维数含偏置M) Yshape（样本数N）
        """
        XMat = np.mat(X)
        YMat = np.mat(Y).T
        self.N, self.M = XMat.shape
        self.W = np.random.rand(self.M, 1)

        for t in range(1, MAX_ITR + 1):
            total_err = 0
            for n in range(self.N):  # each sample
                predict_Y = self.sigmoid(XMat[n] * self.W)
                # 非正式梯度
                err = predict_Y - YMat[n, 0]
                # 梯度
                #err = (predict_Y - YMat[n, 0]) * (1 - predict_Y) * predict_Y
                total_err += np.abs(err)
                self.W = self.W - alpha * XMat[n].T * err
            if t % 10 == 0:
                print t, ':', total_err
        # 训练准确率
        print 'W:', self.W
        return self.W

    def test(self, X, Y):
        XMat = np.mat(X)
        YMat = np.mat(Y).T
        predict_Y = self.sigmoid(XMat * self.W)
        predict_Y[predict_Y > 0.5] = 1
        predict_Y[predict_Y <= 0.5] = 0
        print 'acc', np.sum(predict_Y == YMat) / np.float64(self.N)


import codecs


def prepare_data(filepath):
    X = []
    Y = []
    with codecs.open(filepath, 'r', 'utf-8') as infp:
        for line in infp:
            if not line.strip():
                continue
            # print line.strip().rsplit('\t',1)
            x, y = line.strip().rsplit('\t', 1)
            x = [np.float64(xx) for xx in x.split('\t')]
            y = np.float64(y)
            x.append(1.0)
            X.append(x)
            Y.append(y)
    return X, Y

X, Y = prepare_data('testSet.txt')
L = Logistic()
L.stoc_train(X, Y)
L.test(X, Y)
