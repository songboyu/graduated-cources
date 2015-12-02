# coding=utf-8
import random
import math
import time

import pylab as pl

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__( self ):
		return '(X: {x}, Y:{y})'.format( x = self.x, y = self.y )

	@staticmethod
	def distance( p1, p2 ):
		return math.sqrt( ( p1.x - p2.x ) * ( p1.x - p2.x ) + ( p1.y - p2.y ) * ( p1.y - p2.y ) )

	# <0 : p3在向量 p1p2 下方
	# >0 : p3在向量 p1p2 上方
	@staticmethod
	def CrossMultiply( p1, p2, p3 ):
		return  ( p2.x - p1.x ) * ( p3.y - p1.y ) - ( p2.y - p1.y ) * ( p3.x - p1.x )

def DrawGraph(Q):  
	x,y = [],[]
	for P in Q:
		x.append(P.x)
		y.append(P.y)

	pl.figure(1)  
	pl.subplot(131) #1  
	pl.title(u'蛮力法')  
	pl.xlabel(u'x 轴')  
	pl.ylabel(u'y 轴')  
	pl.plot(x,y,'ro')  

	pl.subplot(132) #2  
	pl.title(u'GrahamScan法')  
	pl.xlabel(u'x 轴')  
	pl.ylabel(u'y 轴')  
	pl.plot(x,y,'ro')  

	pl.subplot(133) #3  
	pl.title(u'分治法')  
	pl.xlabel(u'x 轴')  
	pl.ylabel(u'y 轴')  
	pl.plot(x,y,'ro')

def MakeCHQ(CH):
	x_min = Point(float('inf'), float('inf'))
	x_max = Point(-float('inf'), -float('inf'))

	for P in CH:
		if P.x < x_min.x:
			x_min = P
		if P.x > x_max.x:
			x_max = P
	SU, SL = [],[]
	for P in CH:
		if Point.CrossMultiply(x_min, x_max, P) >= 0:
			SU.append(P)
		else:
			SL.append(P)
	SU.sort(key=lambda x:x.x, reverse=True)
	SL.sort(key=lambda x:x.x, reverse=False)

	CHQ = []
	CHQ.append(x_min)
	CHQ.extend(SL)
	CHQ.append(x_max)
	CHQ.extend(SU)
	return CHQ

def DrawCH(CH):
	CHQ = MakeCHQ(CH)
	print '------------------'
	for P in CHQ:
		print P
	print '------------------'

	x,y=[],[]  
	for P in CHQ:  
		x.append(P.x)  
		y.append(P.y)  
	pl.plot(x,y,color='blue',linewidth=2)  
	pl.plot(x[-1],y[-1],x[0],y[0])  
	lastx=[x[-1],x[0]]  
	lasty=[y[-1],y[0]]  
	pl.plot(lastx,lasty,color='blue',linewidth=2)   #画最后一条封闭线

# 生成x：0-100，y：0-100的方形二维空间内n个点
def MakePoints(n):
	Q = []
	for i in xrange(n):
		x = round(random.uniform(0,100), 3)
		y = round(random.uniform(0,100), 3)
		P = Point(x,y)
		Q.append(P)
	return Q

# 蛮力（枚举）法
def BruteForceCH(Q):
	CH = [P for P in Q]
	# 点P在三角形ABC内或上，返回True，否则返回False
	def PointInnerABC(A, B, C, P):
		PxAB = Point.CrossMultiply(A, B, P)
		PxBC = Point.CrossMultiply(B, C, P)
		PxCA = Point.CrossMultiply(C, A, P)

		CxAB = Point.CrossMultiply(A, B, C)
		AxBC = Point.CrossMultiply(B, C, A)
		BxCA = Point.CrossMultiply(C, A, B)

		return PxAB*CxAB>=0 and PxBC*AxBC>=0 and PxCA*BxCA>=0

	for A in Q:
		for B in Q:
			if B==A: 
				continue
			for C in Q:
				if C==B or C==A: 
					continue
				for P in Q:
					if P==C or P==B or P==A: 
						continue
					# 若p在ABC内或上，则删除P
					PisInABC = PointInnerABC(A,B,C,P)
					if PisInABC:
						try:
							CH.remove(P)
						except:
							pass
	return CH

# Graham算法
def GrahamScanCH(Q):
	Q = [P for P in Q]
	# 比较p1,p2相对于p的极角，若极角 p1 > p2 （p2在向量pp1下方）
	# 或者p、p1、p2一条直线上且pp1 < pp2
	# 则返回1
	def _cmp(p1,p2):
		m = Point.CrossMultiply( SP, p1, p2 )
		if m < 0:
			return 1
		elif m == 0 and Point.distance( SP, p1 ) < Point.distance( SP, p2 ):
			return 1
		else:
			return -1

	SP = Point(float('inf'), float('inf'))
	for P in Q:
		if P.y < SP.y:
			SP = P

	Q.remove(SP)
	# cmp指定一个定制的比较函数，这个函数接收两个参数（iterable的元素）
	# 如果第一个参数小于第二个参数，返回一个负数；
	# 如果第一个参数等于第二个参数，返回零；
	# 如果第一个参数大于第二个参数，返回一个正数。
	# 默认值为None。
	Q = sorted( Q, cmp=_cmp )
	S = []
	S.append(SP)
	S.append(Q[0])
	S.append(Q[1])

	for i in xrange(2,len(Q)):
		while (Point.CrossMultiply( S[-2], S[-1], Q[i] )) <= 0:
			S.pop()
		S.append(Q[i])
	return S

# 分治法
def DivideConquer(Q):
	def Conquer(Q, l, r):
		if r - l <= 2:
			return Q[l:r+1]

		mid = ( l + r ) / 2
		CHL = Conquer(Q, l, mid)
		CHR = Conquer(Q, mid+1, r)
		CH = Merge(CHL,CHR)
		return CH

	def Merge(CHL, CHR):
		QM = []
		QM.extend(CHL)
		QM.extend(CHR)
		CH = GrahamScanCH(QM)
		return CH

	Q.sort(key=lambda x:x.x)
	return Conquer(Q, 0, len(Q)-1)

if __name__ == '__main__':
	Q = MakePoints(20)
	DrawGraph(Q)

	print '-----------蛮力法-----------',len(Q)
	s = time.time()
	CH = BruteForceCH(Q)
	e = time.time()
	print (e - s)*1000,'ms'
	pl.subplot(131)
	DrawCH(CH)

	print '-----------Graham算法-----------',len(Q)
	s = time.time()
	CH = GrahamScanCH(Q)
	e = time.time()
	print (e - s)*1000,'ms'
	pl.subplot(132)
	DrawCH(CH)

	print '-----------分治法-----------',len(Q)
	s = time.time()
	CH = DivideConquer(Q)
	e = time.time()
	print (e - s)*1000,'ms'
	pl.subplot(133)
	DrawCH(CH)

	pl.show() 
