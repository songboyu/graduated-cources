# coding=utf-8

import random
import time
import sys

class Item(object):
	def __init__(self, w, v):
		self.w = w
		self.v = v

	def __repr__(self):
		return '(w: {w}, v:{v})'.format( w = self.w, v = self.v )

# 随机生成物品和背包
def RandomProduce(n, crange):
	C = random.randint(1, crange)
	# C = 200
	items = [None] * n
	for i in xrange(n):
		w = random.randint(1, crange)
		v = random.randint(1, crange)
		item = Item(w,v)
		items[i] = item
	return items, C

# 打印结果
def PrintResult(r):
	u = 0
	v = 0
	for i in xrange(len(r)):
		u += items[r[i]].w
		v += items[r[i]].v
		print i,items[r[i]]
	print u'物品总重：'+str(u),u'物品价值：'+str(v)

# 动态规划算法1
def DynamicProgramming1(items, C):
	def Dynamic(C):
		m = [([None] * (C+1)) for row in xrange(n)]

		for j in xrange(C+1):
			if j < items[n-1].w:
				m[n-1][j] = 0
			else:
				m[n-1][j] = items[n-1].v
		for i in reversed(list(xrange(0, n-1))):
			for j in xrange(C+1):
				if j < items[i].w:
					m[i][j] = m[i+1][j]
				else:
					m[i][j] = max(m[i+1][j], m[i+1][j-items[i].w]+items[i].v)
		return m
	# 构造最优解
	def MakeResult(m):
		j = C
		for i in xrange(n-1):
			if m[i][j] != m[i+1][j]:
				r.append(i)
				j = j - items[i].w
		if m[n-1][j] != 0:
			r.append(n-1)

	n = len(items)
	m = Dynamic(C)
	r = []
	MakeResult(m)
	return r

# 动态规划算法2
def DynamicProgramming2(items, C):
	def Dynamic(Vsum):
		m = [([None] * (Vsum+1)) for row in xrange(n)]

		for j in xrange(Vsum+1):
			if j == 0:
				m[n-1][j] = 0
			elif j > items[n-1].v:
				m[n-1][j] = float("inf")
			else:
				m[n-1][j] = items[n-1].w
		for i in reversed(list(xrange(0, n-1))):
			for j in xrange(Vsum+1):
				if j < items[i].v:
					m[i][j] = m[i+1][j]
				else:
					m[i][j] = min(m[i+1][j], m[i+1][j-items[i].v]+items[i].w)
		return m
	# 构造最优解
	def MakeResult(m):
		j = s
		for i in xrange(n-1):
			if m[i][j] != m[i+1][j]:
				r.append(i)
				j = j - items[i].v
		if m[n-1][j] != float("inf") and m[n-1][j] != 0:
			r.append(n-1)

	# 找到矩阵m中可用的最大V（容量小于C）
	def FindAvailableMaxV(m):
		for j in reversed(xrange(Vsum+1)):
			for i in xrange(n):
				if m[i][j] <= C:
					return j
	Vsum = 0
	for i in items:
		Vsum += i.v

	n = len(items)
	m = Dynamic(Vsum)

	s = FindAvailableMaxV(m)
	r = []
	MakeResult(m)
	return r

# 近似算法
def FPTASApproximation(items, C):
	Vmax = 0
	for i in items:
		if i.v > Vmax:
			Vmax = i.v
	n = len(items)
	# e = random.uniform(0, 1)
	e = 0.9
	K = n / e
	print u'K =',str(K)
	for i in items:
		i.v = int(i.v * ( K / Vmax ))
	r = DynamicProgramming2(items, C)
	return r

if __name__ == '__main__':
	items, C = RandomProduce(100,1000)
	print u'背包容量：'+str(C)
	# 动态规划算法1
	print u'-----------动态规划算法1-----------'
	s = time.time()
	r = DynamicProgramming1(items, C)
	e = time.time()
	print (e - s)*1000,'ms'
	PrintResult(r)
	print

	# 动态规划算法2
	print u'-----------动态规划算法2-----------'
	s = time.time()
	r = DynamicProgramming2(items, C)
	e = time.time()
	print (e - s)*1000,'ms'
	PrintResult(r)
	print

	# 近似算法
	items = [i for i in items]
	print u'-----------近似算法-----------'
	s = time.time()
	r = FPTASApproximation(items, C)
	e = time.time()
	print (e - s)*1000,'ms'
	PrintResult(r)
