# -*- coding: utf-8 -*-

import feedparser
import re

#接受一个博客订阅源，并对内容项进行分类
def read(feed,classifier):
    #f=feedparser.parse('http://kiwitobes.com/feeds/python_search.xml')
    f=feedparser.parse(feed)  #将上面的链接直接存储时会解析出错误的结果
    
    for entry in f['entries']:
        print
        print '-----'
        #打印内容项
        print 'Title:     '+entry['title'].encode('utf-8')
        print 'Publisher: '+entry['publisher'].encode('utf-8')
        print
        print entry['summary'].encode('utf-8')

    
        #将以上所有组合以来组合成内容项
        fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])

        #推测分类
        print 'Guess:  '+str(classifier.classify(entry))

        #请求用户给出一个正确的分类，并据此加以训练
        cl=raw_input('Enter category:   ')
        classifier.train(entry,cl)

#新的特征提取函数，此处输入参数是一个字典，而不是字符串，使用时要注意（特征函数是独立于分类器的）
def entryfeatures(entry):
    splitter=re.compile('\\W*')
    f={}

    #提取出标题中的单词并进行标示
    titlewords=[s.lower() for s in splitter.split(entry['title'])
                if len(s)>2 and len(s)<20]
    for w in titlewords:
        f['Title:'+w]=1

    #抓取摘要中的单词
    summarywords=[s.lower() for s in splitter.split(entry['summary'])
                  if len(s)>2 and len(s)<20]

    #统计大写单词
    uc=0
    for i in range(len(summarywords)):
        w=summarywords[i]
        f[w]=1
        if w.isupper():
            uc+=1

        #将从摘要中获得的词组作为特征
        if i<len(summarywords)-1:
            twowords=' '.join(summarywords[i:i+1])
            f[twowords]=1

    #保持文章创建者和发布者名字的完整性
    f['Publisher:'+entry['publisher']]=1

    #UPPERCASE是个虚拟的单词，用来表示存在过多的大写内容
    #其实summarywords中的全是小写单词，故此处暂时无效
    if float(uc)/len(summarywords)>0.3:
        f['UPPERCASE']=1

    return f


#全局测试代码
import docclass_sqlite as docclass
cl=docclass.fisherclassifier(entryfeatures)
cl.setdb('python_feed.db')
read('python_search.xml',cl)
