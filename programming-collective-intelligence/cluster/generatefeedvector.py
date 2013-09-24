# -*- coding: utf-8 -*-
import feedparser
import re


#返回此RSS订阅源的标题和包含其中单词统计的字典
def getwordcounts(url):
    #解析订阅源
    d=feedparser.parse(url)
    print d.__str__()[1:100]
    if 'bozo_exception' in d.keys():
        print "Can't parser this RSS: %s" % url
        return None,None

    
    wc={}

    #循环遍历文章的所有条目
    for e in d.entries:
        if 'summary' in e:
            summary=e.summary
        else:
            summary=e.description

        #从html中提取出单词列表
        words=getwords(e.title+' '+summary)

        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1

    return d.feed.title,wc

#解析html，返回其中的单词列表
def getwords(html):
    #先去掉html标记，这个和下面那个正则表达式还不大了解，需要深入学习
    txt=re.compile(r'<[^>]+>').sub(' ',html)

    #再利用所有非字母字符拆分出单词
    words=re.compile(r'[^A-Z^a-z]+').split(txt)

    #转化为小写
    return [word.lower() for word in words if word!='']


#主体代码
apcount={} #每个单词出现在几个博客中
wordcounts={}
feedlist=[line for line in file('feedlist.txt')]
print "共读入了 %d 行" % len(feedlist)
curline=1
for feedurl in feedlist:
    print "\n正在解析第 %d 行" % curline
    curline+=1
    title,wc=getwordcounts(feedurl)
    if title==None or wc==None:
        continue
    wordcounts[title]=wc
    for word,count in wc.items():
        apcount.setdefault(word,0)
        if count>1:
            apcount[word]+=1

#去掉过于常见和过于少见的单词
wordlist=[]
for word,bc in apcount.items():
    frac=float(bc)/len(feedlist)
    if frac>0.1 and frac<0.9:
        wordlist.append(word)
#print apcount
print "有效单词数量为：%d" % len(wordlist)

#将统计结果输出到文件中保存起来
out=file('blogdata.txt','w')
out.write('Blog')
#单词列表
for word in wordlist:
    out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')
#不执行close()则文件无法保存
out.close()








    

