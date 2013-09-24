# -*- coding: utf-8 -*-

#一个设计到影评者及其对几步影片评分的字典
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                       'The Night Listener': 3.0},
         'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                          'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                          'You, Me and Dupree': 3.5},
         'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                              'Superman Returns': 3.5, 'The Night Listener': 4.0},
         'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                          'The Night Listener': 4.5, 'Superman Returns': 4.0,
                          'You, Me and Dupree': 2.5},
         'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                          'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                          'You, Me and Dupree': 2.0},
         'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                           'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
         'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt

#求两个人的基于欧几里得距离的相似度评价
def sim_distance(prefs,person1,person2):
    #得到共同物品
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    #无共同项说明两人相似度为0
    if len(si)==0:
        return 0

    #计算差值的平方和
    sum_of_square=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in si])

    #返回0到1之间的数，1表示偏好相同。同时避免被零整除
    return 1/(1+sqrt(sum_of_square))


#皮尔逊相关度函数，它与最佳拟合线密切相关
#比欧几里得计算公式复杂，但是它在数据不是很规范的时候可能会给出更好的结果（修正了夸大分支
def sim_pearson(prefs,person1,person2):
    #获得共同项
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    n=len(si)

    if n==0:
        return 0

    sum1=sum([prefs[person1][item] for item in si])
    sum2=sum([prefs[person2][item] for item in si])

    sum1Sq=sum([pow(prefs[person1][item],2) for item in si])
    sum2Sq=sum([pow(prefs[person2][item],2) for item in si])

    pSum=sum([prefs[person1][item]*prefs[person2][item] for item in si])

    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0:
        return 0

    r=num/den
    return r

#返回与某人品味最相近的n个人
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other)
            for other in prefs if other!=person]

    scores.sort()
    scores.reverse()
    return scores[0:n]
    
#与上面的函数不同，此函数返回的不是person感兴趣的人，而是他感兴趣的东西
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        if other==person:
            continue
        sim=similarity(prefs,person,other)

        #忽略评价值小于等于0的情况
        if sim<=0:
            continue
        for item in prefs[other]:
            #只对自己未观看过的影片进行评价
            if item not in prefs[person] or prefs[person][item]==0:
                #相似度乘以评价值
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                #相似度之和
                simSums.setdefault(item,0)
                simSums[item]+=sim

    #建立一个归一化的列表
    rankings=[(totals[item]/simSums[item],item) for item in totals]
    #这个列表构造貌似比较丑陋
    #rankings=[(total/simSums[item],item) for item,total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings
                
#将字典转置，可以根据一部影片匹配同类影片和寻找潜在的观影者,见测试代码2
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            result[item][person]=prefs[person][item]
    return result


#
#Chapter 2.7: 基于物品的过滤
#构造物品比较数据集，这项工作只需做一次（相当于以空间换时间）
#
def calculateSimilarItems(prefs,n=10):
    #建立字典，以给出与这些物品最为接近的所有其他物品
    result={}

    #以物品为中心将偏好矩阵逆置
    itemPrefs=transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        #如果数据集过大，则每100个item更新下状态
        c+=1
        if c%100==0:
            print "%d / %d" % (c,len(itemPrefs))
        #寻找与item最相近的n个物品
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores
    return result

#为用户推荐物品，输入还包括两个矩阵
def getRecommendedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}

    #循环遍历userRation中user曾经评价的物品
    for (item,rating) in userRatings.items():

        #从itemMatch中获取相近物品
        for (similarity,item2) in itemMatch[item]:

            #如果item2已经被user评价过，则跳过
            if item2 in userRatings:
                continue

            #评价值与相似度加权之和
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating

            #全部相似度之和
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    #相除以归一化
    rankings=[(scores[item]/totalSim[item],item) for item in scores]

    rankings.sort()
    rankings.reverse()
    return rankings


#
#Chapter 2.8: 使用MoviesLens数据集
#使用此数据集来比较基于用户的推荐和基于物品的推荐
#
def loadMovieLens(path=''):
    #获取影片标题
    movies={}
    for line in open('u.item'):
        (id,title)=line.split('|')[0:2]
        movies[id]=title

    #加载数据
    prefs={}
    for line in open('u.data'):
        (user,movieid,rating,ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs
        


#全局测试代码一
if 0:
    print sim_distance(critics,'Lisa Rose','Gene Seymour')
    print sim_pearson(critics,'Lisa Rose','Gene Seymour')
    print topMatches(critics,'Toby',n=3)
    print getRecommendations(critics,'Toby')

#全局测试代码二
if 0:
    movies=transformPrefs(critics)
    #匹配同类影片
    print topMatches(movies,'Superman Returns')
    #寻找潜在观影者
    print getRecommendations(movies,'Just My Luck')

#全局测试代码三
if 0:
    itemsim=calculateSimilarItems(critics)
    print getRecommendedItems(critics,itemsim,'Toby')
    
#全局测试代码四
if 1:
    print "测试 MovieLens 数据集"
    prefs=loadMovieLens()
  #  print prefs['87']

    #基于用户推荐
    print getRecommendations(prefs,'87')[0:30]

    #基于物品推荐（预处理比较慢，但是查询时比上个方法快）
    itemsim=calculateSimilarItems(prefs,n=50)
    print getRecommendedItems(prefs,itemsim,'87')[0:30]
