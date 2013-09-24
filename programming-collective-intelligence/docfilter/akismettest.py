# -*- coding: utf-8 -*-

#Akismet(Automattic Kismet)是应用广泛的一个垃圾留言过滤系统，
#其作者是大名鼎鼎的WordPress创始人Matt Mullenweg，
#Akismet也是WordPress默认安装的插件，其使用非常广泛，
#设计目标便是帮助博客网站来过滤留言spam。有了akismet之后，
#基本上不用担心垃圾留言的烦恼了。

import akismet

defaultkey='033a6edfdb8d'
pageurl='http://www.baidu.com'
defaultagent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en=US; rv=1.8.0.7) "
defaultagent+="Gecko/20060909 Firefix/1.5.0.7"
data = {'user_ip':'114.92.66.199','user_agent':defaultagent}

#调用akismet API判断一段评论是否是垃圾信息
def isspam(comment,author,ipaddress,
           agent=defaultagent,apikey=defaultkey):
    try:
        #传入key和url，另外一种方法是将key和url存到当前目录下的apikey.txt中
        api=akismet.Akismet(key=apikey,blog_url=pageurl,agent=agent)
        valid=api.verify_key()
        
        if valid:
            print "OK. The key is valid"
            return api.comment_check(comment,data)
        else:
            print 'Invalid key'
            return False
    except akismet.AkismetError,e:
        print "AkismetError"
        return False



#测试
if 1:
    msg1='I think the first word is wrong.'
    msg2='Make money fast! Online Casino!'
    msg3='FUCK YOU!!!'
    msg4=''
    print isspam(msg4,None,None)
