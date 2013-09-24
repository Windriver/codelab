# -*- coding: cp936 -*-
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin
import urllib2
import sqlite3
import re

# -*- coding: utf-8 -*-



ignorewords=set(['the','of','to','and','a','in','is','it'])
pagelist=['http://kiwitobes.com/wiki/Perl.html']

class crawler:
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getentryid(self,table,field,value,createnew=True):
        cur=self.con.execute(
            "select rowid from %s where %s='%s'" % (table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute(
                "insert into %s (%s) values ('%s')" % (table,field,value))
            return cur.lastrowid
        else:
            return res[0]

    def addtoindex(self,url,soup):
        if self.isindexed(url):
            return
        print 'Indexing %s' % url

        #get all words in the URL
        text=self.gettextonly(soup)
        words=self.separatewords(text)

        #get the id of URL
        urlid=self.getentryid('urllist','url',url)

        #associate every word with its URL id
        for i in range(len(words)):
            word=words[i]
            if word in ignorewords:
                continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid,wordid,location)\
values (%d,%d,%d)" % (urlid,wordid,i))
                             

    def gettextonly(self,soup):
        v=soup.string
        if v==None:
            c=soup.contents
            resulttext=''
            for t in c:
                subtext=self.gettextonly(t)
                resulttext+=subtext+'\n'
            return resulttext
        else:
            return v.strip()

    def separatewords(self,text):
        splitter=re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!='']

    def isindexed(self,url):
        u=self.con.execute(
            "select rowid from urllist where url='%s'" % url).fetchone()
        if u!=None:
            v=self.con.execute(
                'select *from wordlocation where urlid=%d' % u[0])
            if v!=None:
                return True
        return False

    def addlinkref(self,urlFrom, urlTo,linkText):
        pass

    def crawl(self,pages,depth=2):
        for i in range(depth):
            print "The %i th layer" % i
            newpages=set()
            for page in pages:
                try:
                    c=urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
                    continue
                soup=BeautifulSoup(c.read())
                self.addtoindex(page,soup)

                links=soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url=urljoin(page,link['href'])
                        if url.find("'") != -1:
                            continue
                        
                        url=url.split('#')[0]
                        if url[0:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)

                self.dbcommit()
            pages=newpages

    def createindextables(self):
        self.con.execute('create table if not exists urllist(url)')
        self.con.execute('create table if not exists wordlist(word)')
        self.con.execute('create table if not exists wordlocation(urlid,wordid,location)')
        self.con.execute('create table if not exists link(fromid integer,toid integer)')
        self.con.execute('create table if not exists linkwords(wordid,linkid)')
        
        self.con.execute('create index if not exists wordidx on wordlist(word)')
        self.con.execute('create index if not exists urlidx on urllist(url)')
        self.con.execute('create index if not exists wordurlidx on wordlocation(wordid)')
        self.con.execute('create index if not exists urltoidx on link(toid)')
        self.con.execute('create index if not exists urlfromidx on link(fromid)')
        self.dbcommit()
        
#end of crawler

class searcher:
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self,q):
        #these strings are used to construct the SQL
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]

        #split the query string into words
        words=q.split(' ')
    
        print "Words are splitted into: %s" % words
        tablenumber=0

        for word in words:
            #get ID of word
            sqlquery="select rowid from wordlist where word='%s'" % word
            wordrow=self.con.execute(sqlquery).fetchone()
            
            if wordrow != None:
                wordid=wordrow[0]
                wordids.append(wordid)

                #begin to construct the SQL
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber
                clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
                tablenumber+=1

        if tablenumber == 0:
            print "Invalid query: No valid word"
            return None
        
        fullquery='select %s from %s where %s' % (fieldlist,tablelist,clauselist)
        cur=self.con.execute(fullquery)
        rows=[row for row in cur]

        return rows,wordids

    def getscoredlist(self,rows,wordids):
        totalscores=dict([(row[0],0) for row in rows])

        #weights是个列表，因为对搜索结果的排序是多种因素作用的结果，他们的权重各不相同
        #weights=[]
        #weights=[(1.0,self.frequencyscore(rows))]
        #weights=[(1.0,self.locationscore(rows))]
        weights=[(1.0,self.frequencyscore(rows)),\
                 (1.5,self.locationscore(rows)),\
                 (1.0,self.distancescore(rows))]

        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]

        return totalscores

    def geturlname(self,id):
        return self.con.execute(
            "select url from urllist where rowid=%d" % id).fetchone()[0]
    
    def query(self,q):
        #get the simply processed data
        rows,wordids=self.getmatchrows(q)
        scores=self.getscoredlist(rows,wordids)
        rankedscores=sorted([(score,url) for (url,score) in scores.items()],reverse=1)
        for (score,urlid) in rankedscores[0:10]:
            print '%f\t%s' % (score,self.geturlname(urlid))

    def normalizescores(self,scores,smallIsBetter=0):
        #avoid divided with zero
        vsmall=0.00001
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0:
                maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    #单词频度
    def frequencyscore(self,rows):
        counts=dict([(row[0],0) for row in rows])
        for row in rows:
            #row[0] is URL ID
            counts[row[0]]+=1
        return self.normalizescores(counts)

    #文档位置
    def locationscore(self,rows):
        locations=dict([(row[0],1000000) for row in rows])
        for row in rows:
            loc=sum(row[1:])
            if loc<locations[row[0]]:
                locations[row[0]]=loc
        return self.normalizescores(locations,smallIsBetter=1)

    #单词频度
    def distancescore(self,rows):
        #当值有一个单词时，各URL的得分都一样
        if len(rows)<2:
            return dict([(row[0],1.0) for row in rows])

        #初值预设为极大
        mindistance=dict([(row[0],1000000) for row in rows])

        for row in rows:
            dist=sum([abs(row[i]-row[i-1]) for i in range(2, len(row))])
            if dist<mindistance[row[0]]:
                mindistance[row[0]]=dist
        #这里又缩进错误了，导致只有第一行被统计了
        return self.normalizescores(mindistance,smallIsBetter=1)
  
#crawler=crawler('searchindex.db')
#crawler.createindextables()
#pages=['http://kiwitobes.com/wiki/Categorical_list_of_programming_languages.html']
#crawler.crawl(pages)
#crawler.crawl(['http://java.sun.com/docs/books/jni/html/pitfalls.html'])    
#urlids = [row for row in crawler.con.execute(
#                "select urlid from wordlocation where wordid=6")]
#for urlid in urlids:
#    print crawler.con.execute("select url \
#        from urllist where rowid = %d" % urlid).fetchone()[0]

searcher=searcher('searchindex.db')
print searcher.query("functional programming")

