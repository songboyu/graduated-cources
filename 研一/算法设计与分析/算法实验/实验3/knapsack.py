# coding=utf-8

import random


class Item(object):
	def __init__(self, w, v):
		self.w = w
		self.v = v

	def __repr__(self):
		return '(w: {w}, v:{v})'.format( w = self.w, v = self.v )

# 随机生成物品和背包
def RandomProduce(n, crange):
	C = random.randint(1, crange)
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
		print items[r[i]]
	print '物品总重：'+str(u),'物品价值：'+str(v)
# 动态规划算法
def DynamicProgramming(items, C):
	def Dynamic(C):
		n = len(items)
		m = [([None] * (C+1)) for row in xrange(n)]

		for j in xrange(min(items[n-1].w-1, C)+1):
			m[n-1][j] = 0
		for j in xrange(items[n-1].w, C+1):
			m[n-1][j] = items[n-1].v
		for i in reversed(list(xrange(1, n-1))):
			for j in xrange(min(items[i].w-1, C)+1):
				m[i][j] = m[i+1][j]
			for j in xrange(items[i].w, C+1):
				m[i][j] = max(m[i+1][j], m[i+1][j-items[i].w]+items[i].v)
		if C < items[0].w:
			m[0][C] = m[1][C]
		else:
			m[0][C] = max(m[1][C], m[1][C-items[0].w]+items[0].v)
		return m

	def MakeResult(m, i, j):
		if i == len(items)-1:
			return r
		if m[i][j] == m[i+1][j]:
			MakeResult(m, i+1, j)
		else :
			r.append(i)
			MakeResult(m, i+1, j-items[i].w)

	m = Dynamic(C)
	r = []
	MakeResult(m, 0, C)
	return r

def FPTASApproximation(items, C):
	n = len(items)
	e = random.uniform(0, 1)
	P = 0
	for i in items:
		if i.v > P:
			P = i.v
	K = float(e * P) / n
	print 'K =',str(K)
	for i in items:
		i.v = int(i.v / K)
	r = DynamicProgramming(items, C)
	return r

if __name__ == '__main__':
	items, C = RandomProduce(100,1000)
	print '背包容量：'+str(C)
	# 动态规划算法
	print '-----------动态规划算法-----------'
	r = DynamicProgramming(items, C)
	PrintResult(r)

	# 近似算法
	items = [i for i in items]
	print '-----------近似算法-----------'
	r = FPTASApproximation(items, C)
	PrintResult(r)
