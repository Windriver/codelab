# -*- coding: utf-8 -*-

from pydelicious import get_popular,get_userposts,get_urlposts
import time
#初始化一个包含若干用户名字的字典
def initializeUserDict(tag,count=5):
    user_dict={}
    #获取前count个最受欢迎的张贴记录
    for p1 in get_popular(tag=tag)[0:count]:
        print "Got a post !"
        #查找所有张贴该记录的用户
        #原来的API已经改了，不用href，而是url
        for i in range(3):
            try:
                for p2 in get_urlposts(p1['url']):
                    user=p2['user']
                    user_dict[user]={}
                    break
            except:
                    print "Failed....retrying"
                    time.sleep(4)
    return user_dict

#向上一步初始化的字典内添加内容
def fillItems(user_dict):
    all_items={}
    #查找用户名提交过的连接，并在字典里添加
    for user in user_dict:
        for i in range(3):
            try:
                posts=get_userposts(user)
                break
            except:
                print "Failed user "+user+", retrying"
                time.sleep(4)
        for post in posts:
            url=post['url']
            user_dict[user][url]=1.0
            all_items[url]=1

    #用0填充缺失的项（这一步必要吗？？）
    for ratings in user_dict.values():
        for item in all_items:
            if item not in ratings:
                ratings[item]=0.0


#全局测试代码
if 0:
    pl=get_popular('programming')
    url=pl[0]['url']
    for item in pl:
        url=item['url']
        print url
    for item in pl:
        url=item['url']
        print url
        print get_urlposts(url)
    print get_urlposts('http://www.holub.com/goodies/uml/')
    #print url
   # print get_urlposts(url)

#全局测试代码二
if 0:
   delusers=initializeUserDict('programming')
   #可以向空词典内加入任意相加的用户 
   delusers['tsegaran']={}
   fillItems(delusers)
   #随机选择一位用户
   import random
   user=delusers.keys()[random.randint(0,len(delusers)-1)]
   print user
   import recommendations
   print recommendations.topMatches(delusers,user)


