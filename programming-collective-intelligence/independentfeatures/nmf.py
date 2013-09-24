# -*- coding: utf-8 -*-

from numpy import *

#用以度量最终结果与理想结果的接近程度
def difcost(a,b):
    dif=0
    for i in range(shape(a)[0]):
        for j in range(shape(a)[0]):
            dif+=pow(a[i,j]-b[i,j],2)
    print dif
    return dif


#利用乘法更新法则对矩阵进行因式分解
#经过全局测试代码一，发现此算法非常管用地说！
def factorize(v,pc=10,iter=50):
    ic=shape(v)[0]
    fc=shape(v)[1]

    #用随机值初始化权重矩阵和特征矩阵
    w=matrix([[random.random() for j in range(pc)] for i in range(ic)])
    h=matrix([[random.random() for j in range(fc)] for i in range(pc)])

    #迭代iter次
    for i in range(iter):
        wh=w*h

        cost=difcost(v,wh)
        #print type(cost)
        if i%10==0:
            print cost
        #表示分解已经彻底    
        if cost==0:
            break

        #更新特征矩阵
        hn=(transpose(w)*v)
        hd=(transpose(w)*w*h)
        #print hn
        #print hd
        h=matrix(array(h)*array(hn)/array(hd))

        #更新权重矩阵
        wn=(v*transpose(h))
        wd=(w*h*transpose(h))

        w=matrix(array(w)*array(wn)/array(wd))
        #print w
       # #print h

    return w,h


#全局测试代码一
if 0:
    m1=matrix([[1,2,3],[4,5,6]])
    m2=matrix([[1,2],[3,4],[5,6]])
    print m1
    print m2
    print "m1*m2="
    print m1*m2
    w,h=factorize(m1*m2,pc=3,iter=100)
    print "w*h="
    print w*h
        
