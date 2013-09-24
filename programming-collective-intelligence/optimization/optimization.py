# -*- coding: utf-8 -*-

import time
import random
import math


#姓名与所在地
people=[('Seymour','BOS'),
        ('Franny','DAL'),
        ('Zooey','CAK'),
        ('Walt','MIA'),
        ('Buudy','ORD'),
        ('Les','OMA')]

#会面的地点为New York的Laguardia机场
destination='LGA'

#将航班数据加载到字典里，由起点和终点构成的元组为建，以航班详情三元组构成的列表为值
flights={}

for line in file('schedule.txt'):
    origin,dest,depart,arrive,price=line.strip().split(',')
    flights.setdefault((origin,dest),[]) #默认值为空列表

    #将航班详情添加到航班列表中
    flights[(origin,dest)].append((depart,arrive,int(price)))


#工具函数，用于计算某个给定时间在一天中的分钟数
def getminutes(t):
    x=time.strptime(t,'%H:%M') #解析时间字符串
    return x[3]*60+x[4]


#描述题解，将由一串数字表示的题解打印成列表
def printschedule(r):
    for d in range(len(r)/2):
        name=people[d][0]
        origin=people[d][1]
        out=flights[(origin,destination)][r[2*d]]
        ret=flights[(destination,origin)][r[2*d+1]]
        print "%10s%10s %5s-%5s $%3s %5s-%5s $%3s" % (name,origin,
                                                      out[0],out[1],out[2],
                                                      ret[0],ret[1],ret[2])


#成本函数是优化算法的关键，也是最难确定的。我们最终想获得一个使优化函数的值最小的输入。
def schedulecost(sol):
    totalprice=0
    lastestarrival=0
    earliestdep=24*60

    for d in range(len(sol)/2):
        #得到往程航班和返程航班
        origin=people[d][1]
        outbound=flights[(origin,destination)][sol[2*d]]
        returnf=flights[(destination,origin)][sol[2*d+1]]

        #计算总价格
        totalprice+=outbound[2]
        totalprice+=returnf[2]

        #记录下最晚到达时间和最早离开时间
        if lastestarrival<getminutes(outbound[1]):
            out=outbound[1]
            lastestarrival=getminutes(outbound[1])
        if earliestdep>getminutes(returnf[0]):
            dep=returnf[0]
            earliestdep=getminutes(returnf[0])

    #每个人必须在机场等待直到最后一个人到达为止
    #也必须在相同时间到达，并等候他们的返程航班
    totalwait=0
    for d in range(len(sol)/2):
        origin=people[d][1]
        outbound=flights[(origin,destination)][sol[2*d]]
        returnf=flights[(destination,origin)][sol[2*d+1]]
        totalwait+=lastestarrival-getminutes(outbound[1])
        totalwait+=getminutes(returnf[0])-earliestdep

    #要多付一天的出租车费用吗?
    if lastestarrival>earliestdep:
        totalprice+=50

    return totalprice+totalwait
        

#随机搜索并不是一种非常好的优化算法，但它可以作为评估其他算法优劣的基线baseline
def randomoptimize(domain,costf):
    best=999999999
    bestr=None
   
    for i in range(1000):
        #创建一个随机解
        r=[random.randint(domain[i][0],domain[i][1])
           for i in range(len(domain))]

        #获取成本
        cost=costf(r)
        
        if cost<best:
            best=cost
            bestr=r
    return bestr #这里应该返回bestr而不是r，书上写错了


#爬山法
#从一个随机解开始，然后在它的临近的解集中寻找更好的题解（具有更低的成本），类似于从斜坡向下走
#经过测试发现爬山法的优化效果明显比随机优化要好，但是它获得的是一个局部范围内的最小值
def hillclimb(domain,costf):
    #创建一个随机解
    sol=[random.randint(domain[i][0],domain[i][1])
         for i in range(len(domain))]

    #主循环
    while 1:
        #创建相邻解集的列表
        neighbors=[]
        for j in range(len(domain)):
            #每个方向都偏离一次并加入列表
            if sol[j]>domain[j][0]:
                neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
            if sol[j]<domain[j][1]:
                neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])

        #在相邻解集中寻找最优解
        current=costf(sol)
        best=current
        for j in range(len(neighbors)):
            cost=costf(neighbors[j])
            if cost<best:
                best=cost
                sol=neighbors[j]

        if best==current: #表示解集中没有更好的解
            break

    return sol


#模拟退火算法
#算法从一个随机解开始。初始温度非常之高，表示接受较差解的意愿也很高，随着温度的递减，算法越来越不可能接受较差的解
#结果测试发现模拟退火的优化效果很不稳定，几乎总是弱于爬山法，跟书上的不一样。
#调试时发现，可能是公式的参数有问题，导致当前最优解经常被较差解替代。
#于是我便修改参数，发现T=1000,cool=0.99是，结果为3200左右，当进一步把cool改为0.999时，结果为2500左右

def annealingoptimize(domain,costf,T=100000.0,cool=0.99,step=1):
    #随机初始化值
    vec=[random.randint(domain[i][0],domain[i][1])
         for i in range(len(domain))]

    while T>0.1:
        #选择一个索引值
        i=random.randint(0,len(domain)-1)

        #选择一个改变索引值的方向，下式只会返回整数
        dir=random.randint(-step,step)

        #创建新解，并改变其中一个值
        vecb=vec[:]
        vecb[i]+=dir
        if vecb[i]<domain[i][0]:
            vecb[i]=domain[i][0]
        elif vecb[i]>domain[i][1]:
            vecb[i]=domain[i][1]

        #计算当前成本和新成本
        ea=costf(vec)
        #print ea
        eb=costf(vecb)

        #它是更好的解吗？或者是趋向最优解的可能的临界解吗？
        if (eb<ea or random.random()<pow(math.e,-(eb-ea)/T)):
            #if eb>=ea:
             #   print pow(math.e,-(eb-ea)/T)

            # eb
            vec=vecb

        #降低温度
        T=T*cool
    #print T
    return vec


#遗传算法
#先随机构造出初始种群，每次迭代都根据评价函数进行排序，按照精英率进行精英选拔，
#再在精英的基础上进行交叉变异，使种群大小不变
#测试发现，遗传算法很有效，能很快地降低成本，并且种群大小越大，效果越好
#但是下面这个实现的问题是迭代几代以后，成本就稳定不变了，说明变异并未带来更优秀的个体，也可能是本问题的特点导致的
def geneticoptimize(domain,costf,popsize=50,step=1,
                    mutprob=0.2,elite=0.2,maxiter=100):
    #内部子函数：变异操作 (书上函数有错误，漏掉一种达到上界的情况，导致返回None）
    #其实这个函数很丑陋，应该先随机确定增加还是减少，再考虑边界情况
    def mutate(vec):
        i=random.randint(0,len(domain)-1)
        if random.random()<0.5 and vec[i]>domain[i][0]: #该分支有50%几率无法接收达到上界的情况
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif vec[i]<domain[i][1]: #达到下届的情况由这一分支接收，
            return vec[0:i]+[vec[i]+step]+vec[i+1:]
        elif vec[i]==domain[i][1]:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        else:
            return vec

    #内部子函数：交叉操作
    def crossover(r1,r2):
        i=random.randint(1,len(domain)-2) #注意上下限，都缩减了1，为的是能真正产生变异
        return r1[0:i]+r2[i:]

    #构造初始种群
    pop=[]
    for i in range(popsize):
        vec=[random.randint(domain[i][0],domain[i][1])
             for i in range(len(domain))]
        pop.append(vec)

    #每一代有多少胜出者
    topelite=int(popsize*elite)

    #主循环
    for i in range(maxiter):
        scores=[(costf(v),v) for v in pop]
        scores.sort()
        ranked=[v for (s,v) in scores]

        #从纯粹的胜出者开始
        pop=ranked[0:topelite]

        #添加变异和配对后的胜出者
        while len(pop)<popsize:
            if random.random()<mutprob: #变异率在此体现
                c=random.randint(0,topelite)
                newv=mutate(ranked[c])
                pop.append(newv)
                #print newv ,"mut"
            else:
                #剩下的由交叉产生
                c1=random.randint(0,topelite)
                c2=random.randint(0,topelite)
                newv=crossover(ranked[c1],ranked[c2])
                pop.append(newv)
                #print newv ,"cross"

        #打印当前最优值
        print scores[0][0]
    return scores[0][1]
        


#全局测试代码一
if 0:
    
    domain=[(0,9)]*(len(people)*2)
    #随机优化
    #s=randomoptimize(domain,schedulecost)
    #爬山法
    #s=hillclimb(domain,schedulecost)
    #模拟退火
    #s=annealingoptimize(domain,schedulecost)
    #遗传算法
    s=geneticoptimize(domain,schedulecost)
    print schedulecost(s)
    printschedule(s)

    

    

