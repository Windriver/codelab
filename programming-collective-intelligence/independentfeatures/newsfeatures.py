# -*- coding: utf-8 -*-


import feedparser
import re

#新闻来源
feedlist=['http://feeds.reuters.com/reuters/topNews', #改
          'http://feeds.reuters.com/Reuters/domesticNews', #改
          'http://feeds.reuters.com/Reuters/worldNews', #改
          #'http://hosted.ap.org/lineups/TOPHEADS-rss_2.0.xml',
          #'http://hosted.ap.org/lineups/USHEADS-rss_2.0.xml',
          #'http://hosted.ap.org/lineups/WORLDHEADS-rss_2.0.xml',
          #'http://hosted.ap.org/lineups/POLITICSHEADS-rss_2.0.xml',
          'http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml',
          'http://www.nytimes.com/services/xml/rss/nyt/International.xml',
          #'http://news.google.com/?output=rss', #弃
          'http://www.salon.com/feed/', #改
          'http://www.foxnews.com/xmlfeed/rss/0,4313,0,00.rss',
          'http://www.foxnews.com/xmlfeed/rss/0,4313,80,00.rss',
          'http://www.foxnews.com/xmlfeed/rss/0,4313,81,00.rss',
          'http://rss.cnn.com/rss/edition.rss',
          'http://rss.cnn.com/rss/edition_world.rss',
          'http://rss.cnn.com/rss/edition_us.rss'
          #新增
          'http://pheedo.msnbc.msn.com/id/3032091/device/rss',
          'http://rss.msnbc.msn.com/id/3032524/device/rss/rss.xml',
          'http://rss.msnbc.msn.com/id/3032506/device/rss/rss.xml',
          'http://rss.msnbc.msn.com/id/3032552/device/rss/rss.xml',
          'http://rss.msnbc.msn.com/id/3032071/device/rss/rss.xml']


#处理HTML文件，可以去掉其中的所有标签和图片
def stripHTML(h):
    p=''
    s=0
    for c in h: #遍历每个字母,根据情况对字母执行不同的操作
        if c=='<':
            s=1
        elif c=='>':
            s=0
            p+=' '
        elif s==0:
            p+=c

    return p

#拆分文本中的单词
def separatewords(text):
    splitter=re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s)>3]

#遍历订阅源，记录每个单词在所有文章中总共被使用的次数，以及在每篇文章中使用的次数
def getarticlewords():
    allwords={}
    articlewords=[]
    articletitles=[]
    ec=0 #文章计数器
    #遍历每个订阅源
    for feed in feedlist:
        print feed
        f=feedparser.parse(feed)
        #print f
        #遍历该订阅源中的每篇文章
        for e in f.entries:
            #跳过标题相同的文章
            if e.title in articletitles:
                continue

            #提取单词
            txt=e.title.encode('utf8')+stripHTML(e.description).encode('utf8')
            words=separatewords(txt)
            articlewords.append({}) #该列表的元素为字典
            articletitles.append(e.title)

            for word in words:
                allwords.setdefault(word,0)
                allwords[word]+=1
                articlewords[ec].setdefault(word,0)
                articlewords[ec][word]+=1
            ec+=1
        print 'ec='+ec.__str__()
    return allwords,articlewords,articletitles
                
#构造单词矩阵
def makematrix(allw,articlew):
    wordvec=[]

    for w,c in allw.items():
        if c>3 and c<len(articlew)*0.6:
            wordvec.append(w)

    l1=[[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
    return l1,wordvec    

#全局测试代码一
if 0:
    allw,artw,artt=getarticlewords()
    wordmatrix,wordvec=makematrix(allw,artw)
    print wordvec[0:10]
    print artt[1]
    print wordmatrix[1][0:100]
    
