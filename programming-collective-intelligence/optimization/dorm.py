# -*- coding: utf-8 -*-

import random
import math

#代表宿舍，每个宿舍有两个可用的隔间
dorms=['Zeus','Athena','Hercules','Bacchus','Pluto']

#代表学生及其首选宿舍和次选
prefs=[('Toby',('Bacchus','Hercules')),
       ('Steve',('Zeus','Pluto')),
       ('Andrea',('Athena','Zeus')),
       ('Sarah',('Zeus','Pluto')),
       ('Dave',('Athena','Bacchus')),
       ('Jeff',('Hercules','Pluto')),
       ('Fred',('Pluto','Athena')),
       ('Suzie',('Bacchus','Hercules')),
       ('Laura',('Bacchus','Hercules')),
       ('Neil',('Hercules','Athena'))]

#本题的题解表示法，第一位可置于10个槽中的任何一个内，第二位则可置于剩余9个槽中的任何一个内，依此类推
domain=[(0,(len(dorms))*2-i-1) for i in range(0,len(dorms)*2)]


#打印结果。只要题解符合domain，则一定是合理的解
def printsolution(vec):
    slots=[]
    #为每个宿舍分配两个槽
    for i in range(len(dorms)):
        slots+=[i,i]
    
    #遍历每个学生的安置情况，每安排一个学生，总槽数减1
    for i in range(len(vec)):
        #获得第i个学生的空槽位
        x=int(vec[i])

        #从剩余槽中选择
        dorm=dorms[slots[x]]
        #输出学生及其被分配的宿舍
        print prefs[i][0],dorm
        #删除该槽
        del slots[x]


#成本函数
def dormcost(vec):
    cost=0
    #建立一个槽序列
    slots=[0,0,1,1,2,2,3,3,4,4]

    #遍历每一个学生
    for i in range(len(vec)):
        x=int(vec[i])
        dorm=dorms[slots[x]]
        pref=prefs[i][1]
        #算出每位学生的成本值
        if pref[0]==dorm:
            cost+=0
        elif pref[1]==dorm:
            cost+=1
        else:
            cost+=3

        del slots[x]

    return cost



#全局测试代码
if 0:
    import optimization
    print "genetic"
    optimization.geneticoptimize(domain,dormcost)
    
    print "random"
    s=optimization.randomoptimize(domain,dormcost)
    print dormcost(s)
    printsolution(s)
