# -*- coding: utf-8 -*-
import sqlite3
import re
import math

#抽取一篇文档的特征（此处为不重复的单词）
def getwords(doc):
    splitter=re.compile('\\W*')
    #根据非字母字符将文档拆分为单词
    words=[s.lower() for s in splitter.split(doc)
           if len(s)>2 and len(s)<20]

    return dict([(w,1) for w in words])

#样本训练函数（省的每次都输入训练数据）
def sampletrain(cl):
    cl.train('Nobody owns the water','good')
    cl.train('the quick rabbit jumps fences','good')
    cl.train('buy pharmaceuticals now','bad')
    cl.train('make quick money at the online casino','bad')
    cl.train('the quick brown fox jumps','good')

#这个是分类器基类
class classifier:
    def __init__(self,getfeatures,filename=None):
        #统计特征/分类组合的数量
        self.fc={}
        #统计每个分类中文档的数量
        self.cc={}
        self.getfeatures=getfeatures

    #新建与数据库的连接，并新建两个表用来替代以前的字典
    def setdb(self,dbfile):
        self.con=sqlite3.connect(dbfile)
        self.con.execute('create table if not exists fc(feature,category,count)')
        self.con.execute('create table if not exists cc(category,count)')

    #增加对特征/分类组合的计数值
    def incf(self,f,cat):
        count=self.fcount(f,cat)
        if count==0:
            self.con.execute("insert into fc values('%s','%s',1)" % (f,cat))
        else:
            self.con.execute("update fc set count=%d where feature='%s' and category='%s'"
                             % (count+1,f,cat))

    #增加某一分类的计数值
    def incc(self,cat):
        count=self.catcount(cat)
        if count==0:
            self.con.execute("insert into cc values('%s','%s')" % (cat,1))
        else:
            self.con.execute("update cc set count=%d where category='%s'" % (count+1,cat))

    #某一特征出现于某一分类的次数（即fc字典的基本用法）
    def fcount(self,f,cat):
        res=self.con.execute("select count from fc where feature='%s' and category='%s'"
                             % (f,cat)).fetchone()
        if res==None:
            return 0
        else:
            return float(res[0])

    #属于某一分类的内容项数量(即cc字典的基本用法）
    def catcount(self,cat):
        res=self.con.execute("select count from cc where category='%s'" % cat).fetchone()
        if res==None:
            return 0
        else:
            return float(res[0])

    #所有内容项（文档）的数量
    def totalcount(self):
        res=self.con.execute("select sum(count) from cc").fetchone()
        if res==None:
            return 0
        else:
            return res[0]

    #所有分类的列表
    def categories(self):
        #这里用查询后得到的游标
        cur=self.con.execute("select category from cc")
        return [d[0] for d in cur]

    #以内容项和它的分类作为参数进行训练
    def train(self,item,cat):
        features=self.getfeatures(item)
        #对该分类的每一个特征增加计数值
        for f in features:
            self.incf(f,cat)
            
        #对属于该分类的内容项计数值加1
        self.incc(cat)
        self.con.commit()

    #计算特征(即单词)在某分类中出现的概率
    #记作Pr(A|B)，读作“在给定B的条件下A的概率,这里为Pr(word|classfication)
    def fprob(self,f,cat):
        if self.catcount(cat)==0:
            return 0
        return self.fcount(f,cat)/self.catcount(cat)

    #当样本有限时，可以设一个初始的推荐值，并给它一个权重（ap和weight)
    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        #计算基础的概率值,这里使用传入的prf增加可重用性
        basicprob=prf(f,cat)

        #统计特征在所有分类中出现的次数
        totals=sum([self.fcount(f,c) for c in self.categories()])

        #计算加权平均
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp
    

#朴素贝叶斯分类器继承自上面的分类器
#之所以叫朴素，是因为它假设将要被组合的各个概率是彼此独立的
class naivebayes(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.thresholds={}
        
    #提取出所有特征，并将它们的概率相乘,求得了Pr(Document|Category)
    def docprob(self,item,cat):
        features=self.getfeatures(item)
        p=1
        for f in features:
            p*=self.weightedprob(f,cat,self.fprob)
        return p

    #根据贝叶斯定理，通过调换求解，求得已知文档求其所属分类的概率
    def prob(self,item,cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item,cat)
        return catprob*docprob
    
    #设置和取得某一个分类阈值
    def setthresholds(self,cat,t):
        self.thresholds[cat]=t
        
    def getthresholds(self,cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    #对内容项进行分类的函数
    def classify(self,item,default=None):
        probs={}
        #寻找概率最大的分类
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat

        #确保这个best符合阈值
        for cat in probs:
            if cat==best:
                continue
            if probs[cat]*self.getthresholds(best)>probs[best]:
                return default
        return best

#
#费舍尔方法
class fisherclassifier(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.minimums={} #用来保存临界值
        
    #针对特征的分类概率
    def cprob(self,f,cat):
        clf=self.fprob(f,cat)
        if clf==0:
            return 0

        #特征在各个分类中的出现概率之和
        freqsum=sum([self.fprob(f,c) for c in self.categories()])

        p=clf/freqsum
        return p

    #将各个概率值组合起来
    def fisherprob(self,item,cat):
        p=1
        features=self.getfeatures(item)
        for f in features:
            p*=(self.weightedprob(f,cat,self.cprob))

        #取自然对数，并乘以-2
        fscore=-2*math.log(p)

        #利用倒置对数卡方函数求得概率
        return self.invchi2(fscore,len(features)*2)

    #费舍尔方法告诉我们，如果概率彼此独立且随机分布，则这一计算结果满足对数卡方分布(chi-squared distribution)
    def invchi2(self,chi,df):
        m=chi/2.0
        sum=term=math.exp(-m)
        for i in range(1,df/2):
            term*=m/i
            sum+=term
        return min(sum,1.0)
                
    def setminimum(self,cat,min):
        self.minimums[cat]=min

    def getminimum(self,cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]

    def classify(self,item,default=None):
        #遍历寻找最佳结果
        best=default
        max=0.0
        for c in self.categories():
            p=self.fisherprob(item,c)
            #确保超过下限值
            if p>self.getminimum(c) and p>max:
                best=c
                max=p
                
        return best
            
    
#全局测试代码

#测试sqlite
if 0:
    cl=fisherclassifier(getwords)
    cl.setdb('test1.db')
    sampletrain(cl)
    cl2=naivebayes(getwords)
    cl2.setdb('test1.db')
    print cl2.classify('quick fox')
