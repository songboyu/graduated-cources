#coding: utf-8
import time
import random

import numpy as np
import cPickle
import matplotlib.pyplot as plt
import scipy.io as sio

class KMeans(object):
    """
    - 参数
        k:
            聚类个数，即k
        max_iter:
            最大迭代次数
    """
    def __init__(self, k=5, max_iter=300):
        self.k = k
        self.max_iter = max_iter

        self.clusterAssment = None
        self.labels = None   
        self.SSE = None 
    
    # 计算两点的欧式距离
    def EuclideanDist(self, vectorA, vectorB):
        return np.sqrt(np.sum((vectorA - vectorB) ** 2))
        
    # 初始时随机选取k个质心
    def initCentroids(self, data, k):
        # m行n列
        m, n = data.shape
        #k*n的矩阵，用于存储质心
        centroids = np.empty((k, n))  
        
        for i in range(k):
            index = random.randint(0, m)
            centroids[i, :] = data[index-1, :]
        return centroids
        
    def fit(self, data):
        m, n = data.shape
        # m*2的矩阵，第一列：存储样本点所属的簇下标，
        #           第二列：存储该点与所属族的质心的平方误差
        self.clusterAssment = np.empty((m,2))
        self.centroids = self.initCentroids(data, self.k)
        
        clusterChanged = True
        for _ in range(self.max_iter):
            clusterChanged = False
            # 将每个样本点分配到离它最近的质心所属的族
            for i in range(m):
                minDist = np.inf
                minIndex = -1
                for j in range(self.k):
                    distance = self.EuclideanDist(self.centroids[j,:], data[i,:])
                    if distance < minDist:
                        minDist = distance
                        minIndex = j
                # 如果点i分配到与上次不同的簇，则说明簇发生变化
                if self.clusterAssment[i,0] != minIndex:
                    clusterChanged = True
                    self.clusterAssment[i,:] = minIndex,minDist**2

            # 若所有样本点所属的族都不改变,则已收敛，结束迭代
            if not clusterChanged:
                break   
            # 更新质心，即将每个族中的点的均值作为质心
            for i in range(self.k):
                # 取出属于第i个簇的所有点
                ptsInClust = data[np.nonzero(self.clusterAssment[:,0]==i)[0]]
                self.centroids[i,:] = np.mean(ptsInClust, axis=0)
        
        self.labels = self.clusterAssment[:,0]
        self.SSE = sum(self.clusterAssment[:,1])

def process(data, k):
    max_iter = 10
    clf = KMeans(k, max_iter)
    clf.fit(data)
    centroids = clf.centroids
    labels = clf.labels

    # 画出聚类结果，每一类用一种颜色
    colors = ['b','g','r','c','m']
    for i in range(k):
        index = np.nonzero(labels==i)[0]
        x = data[index,0]
        y = data[index,1]

        plt.plot(x, y, colors[i]+'.')
        plt.plot(centroids[i,0], centroids[i,1], 'k+', markersize=10, markeredgewidth=1)
    plt.title("SSE={:.2f}".format(clf.SSE))

if __name__ == "__main__":
    plt.figure(1)
    # 环形
    data = sio.loadmat('../data/ThreeCircles.mat')['ThreeCircles']
    data = data[:,1:3]
    k = 3
    plt.subplot(231)
    process(data, k)

    # 双月牙形
    data = sio.loadmat('../data/Twomoons.mat')['Twomoons']
    data = data[:,1:3]
    k = 2
    plt.subplot(232)
    process(data, k)

    # 螺旋线（密度相同）
    data = sio.loadmat('../data/spiral.mat')['spiral']
    data = data[:,1:3]
    k = 2
    plt.subplot(233)
    process(data, k)

    # 二维2簇
    data = sio.loadmat('../data/2_cluster.mat')['X']
    data = np.transpose(data)
    k = 2
    plt.subplot(234)
    process(data, k)

    # 二维3簇
    data = sio.loadmat('../data/3_cluster.mat')['X']
    data = np.transpose(data)
    k = 3
    plt.subplot(235)
    process(data, k)

    # 二维5簇
    data = sio.loadmat('../data/5_cluster.mat')['x']
    data = np.transpose(data)
    k = 5
    plt.subplot(236)
    process(data, k)

    plt.show()
