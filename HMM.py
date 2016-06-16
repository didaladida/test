
# coding: utf-8

# In[118]:


import numpy as np
"""
概率的计算
"""


def calc_prob_O_pro(A, B, pi, O):
    """
    给定HMM参数 lambda=(A,B,calc_prob_O_pro(A,B,pi,O)pi) 计算状态序列 O的概率  前向算法
    """
    # dp[i][t] 时刻t处在状态i 且表表现为希望的子序列的概率
    dp = np.empty((A.shape[0], O.shape[0]))  # dp数组
    AMat = np.mat(A)
    BMat = np.mat(B)
    piMat = np.mat(pi)
    OMat = np.mat(O)
    dpMat = np.mat(dp)
    # 设置初始值
    dpMat[:, 0] = np.multiply(piMat.T, BMat[:, O[0]])
    print dpMat[:, 0]
    for i in range(1, O.shape[0]):
        stats_dis = dpMat[:, i - 1].T * AMat
        dpMat[:, i] = np.multiply(stats_dis.T, BMat[:, O[i]])
        print dpMat[:, i]
    # dp dpMat 是同一个数据源
    # so  the  same
    # return np.sum(dp[:,-1])
    return np.sum(dpMat[:, -1]), dpMat


def calc_prob_O_back(A, B, pi, O):
    """
    给定HMM参数 lambda=(A,B,pi) 计算状态序列 O的概率  后向算法
    """
    T = O.shape[0]
    n = A.shape[0]
    dp = np.empty((n, T))  # dp数组
    AMat = np.mat(A)
    BMat = np.mat(B)
    piMat = np.mat(pi)
    OMat = np.mat(O)
    dpMat = np.mat(dp)
    # 初始化
    dpMat[:, -1] = 1
    for t in range(T - 2, -1, -1):
        dpMat[:, t] = AMat * np.multiply(BMat[:, O[t + 1]], dpMat[:, t + 1])
        print dpMat[:, t]
    ans = np.multiply(dpMat[:, 0], piMat.T)
    ans = np.multiply(ans, BMat[:, O[0]])
    # 错误  第三个参数未相乘
    # ans=np.multiply(dpMat[:,0],piMat.T,BMat[:,O[0]])
    return np.sum(ans), dpMat


# test  from  统计机器学习
# x,a= calc_prob_O_pro(np.array([[0.5,0.2,0.3],[0.3,0.5,0.2],[0.2,0.3,0.5]]),np.array([[0.5,0.5],[0.4,0.6],[0.7,0.3]]),
#           np.array([0.2,0.4,0.4]),np.array([0,1,0]))
# y,b= calc_prob_O_back(np.array([[0.5,0.2,0.3],[0.3,0.5,0.2],[0.2,0.3,0.5]]),np.array([[0.5,0.5],[0.4,0.6],[0.7,0.3]]),
#           np.array([0.2,0.4,0.4]),np.array([0,1,0]))
# np.sum(np.multiply(a[:,0],b[:,0]))

"""
预测的近似算法
"""


def prox(A, B, pi, O):
    print u'计算前向后向概率矩阵'
    p, pre = calc_prob_O_pro(A, B, pi, O)
    p, back = calc_prob_O_back(A, B, pi, O)
    T = O.shape[0]
    print u'计算路径'
    tmp = np.multiply(pre, back)
    tmp = np.argmax(tmp, axis=0)   
    tmp += 1
    path = np.array(tmp)
    return path


"""
HMM预测算法
"""


def viterbi(A, B, pi, O):
    """
    维特比预测状态序列算法
    """
    AMat = np.mat(A)
    BMat = np.mat(B)
    piMat = np.mat(pi)
    T = O.shape[0]
    N = A.shape[0]
    sigma = np.empty((N, T))
    fi = np.empty((N, T))
    sigmaMat = np.mat(sigma)
    fiMat = np.mat(fi)
    # 初始化
    sigmaMat[:, 0] = np.multiply(piMat.T, BMat[:, O[0]])
    # print sigmaMat[:,0]
    fiMat[:, 0] = 0
    for t in range(1, T):
        # print AMat
        # print sigmaMat[:,t-1]
        tmp = np.multiply(AMat, sigmaMat[:, t - 1])
        # print tmp
        # print np.argmax(tmp,axis=0)+1
        fiMat[:, t] = np.argmax(tmp, axis=0).T
        tmp = np.max(tmp, axis=0)
        sigmaMat[:, t] = np.multiply(tmp.T, BMat[:, O[t]])
        # print sigmaMat[:,t]

    P_star = np.max(sigmaMat[:, -1])  # 最有路径的概率
    stat = np.argmax(sigmaMat[:, -1])
    path = np.empty(T)
    path[T - 1] = stat
    for t in range(T - 1, 0, -1):
        path[t - 1] = (fiMat[stat, t])
        stat = fiMat[stat, t]
    # 计算过程中状态以0开始，书中以1开始
    path += 1
    return P_star, path


print u'近似算法'
print prox(np.array([[0.5, 0.2, 0.3], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]]), np.array([[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]]),
     np.array([0.2, 0.4, 0.4]), np.array([0, 1, 0]))
print u'viterbi'
viterbi(np.array([[0.5, 0.2, 0.3], [0.3, 0.5, 0.2], [0.2, 0.3, 0.5]]), np.array([[0.5, 0.5], [0.4, 0.6], [0.7, 0.3]]),
        np.array([0.2, 0.4, 0.4]), np.array([0, 1, 0]))


# In[64]:




# In[92]:




