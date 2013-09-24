# -*- coding: utf-8 -*-

from random import random,randint
import math

#根据酒的等级和储藏的年代来决定酒的价格
def wineprice(rating,age):
    peak_age=rating-50

    price=rating/2
    if age>peak_age:
        #经过“峰值年”，后继5年其品质将会变差
        price=price*(5-(age-peak_age))
    else:
        #价格在接近“峰值年”时会增加到原值的5倍
        price=price*(5*((age+1)/peak_age))
    if price<0:
        price=0
    return price

#用此函数“生产”了200瓶葡萄酒
def wineset1():
    rows=[]
    for i in range(300):
        #随机生成年代和等级
        rating=random()*50+50
        age=random()*50

        #得到一个参考价格
        price=wineprice(rating,age)

        #增加噪声
        price*=(random()*0.4+0.8)

        #加入数据集
        rows.append({'input':(rating,age),
                     'result':price})

    return rows


#用欧几里得距离算法定义两件商品之间的相似度
def euclidean(v1,v2):
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2
    return math.sqrt(d)

#K最近邻算法（KNN）
def getdistances(data,vec1):
    distancelist=[]
    for i in range(len(data)):
        vec2=data[i]['input']
        distancelist.append((euclidean(vec1,vec2),i))
    distancelist.sort()
    return distancelist

def knnestimate(data,vec1,k=5):
    #结果排序得到的距离值
    dlist=getdistances(data,vec1)
    avg=0.0

    #对前k项结果求平均值
    for i in range(k):
        idx=dlist[i][1]
        avg+=data[idx]['result']
    avg=avg/k
    return avg

#
#chapter 8.3:为近邻分配权重
#普通的KNN可能选择距离太远的近邻，一种补偿的方法是根据距离的远近为其赋以响应的权重
#

#距离转换成权重的方法1：反函数
def inverseweight(dist,num=1.0,const=0.1):
    return num/(dist+const)

#方法2：减法函数
def substractweight(dist,const=1.0):
    if dist>const:
        return 0
    else:
        return const-dist

#方法3：高斯函数
#测试时发现高斯函数得到的结果偏大。这是我应该仔细研究公式，研究函数曲线，并换其他的自变量试下，结果发现是中文版的印刷错误。
def gaussian(dist,sigma=10.0):
    return math.e**(-dist**2/(2*sigma**2))

#加权KNN
def weightedknn(data,vec1,k=5,weightf=gaussian):
    #得到距离值
    dlist=getdistances(data,vec1)
    avg=0.0
    totalweight=0.0

    #得到加权平均值
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg+=weight*data[idx]['result']
        totalweight+=weight
    avg=avg/totalweight
    return avg

#全局测试代码一
if 0:
    print wineprice(95.0,3.0)
    print wineprice(95.0,8.0)
    print wineprice(99.0,1.0)
    data=wineset1()
    print data[0]
    print data[1]
    print euclidean(data[0]['input'],data[1]['input'])

#全局测试代码二
if 1:
    data=wineset1()
    print knnestimate(data,(95.0,3.0))
    print knnestimate(data,(99.0,3.0))
    print "Test KNN"
    print knnestimate(data,(99.0,5.0))
    print "Right value"
    print wineprice(99.0,5.0)
    print "less neighber, k=1"
    print knnestimate(data,(99.0,5.0),k=1) #结果比较，发现k=5比k=1时的KNN算法更加精确
    print "Test weighted KNN"
    print weightedknn(data,(99.0,5.0))
