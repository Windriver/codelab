# -*- coding: utf-8 -*-

import urllib2
import xml.dom.minidom

api_key="479NUNJHETN"

#获取一个随机的人员列表，用来构造数据集
def getrandomratings(c):
    #构造URL
    url="http://services.hotornot.com/rest/?app_key=%s" % api_key
    url+="&method=Rate.getRandomProfile&retrieve_num=%d" % c
    url+="&get_rate_info=true&meet_users_only=true"

    fl=urllib2.urlopen(url).read()

    doc=xml.dom.minidom.parseString(fl)

    emid=doc.getElementsByTagName('emid')
    ratrings=doc.getElementsByTagName('rating')

    #将emids和ratings组合到一个列表
    #zip()是Python的一个内建函数，它接受一系列可迭代的对象作为参数，
    #将对象中对应的元素打包成一个个tuple（元组），然后返回由这些tuples组成的list（列表）
    result=[]
    for e,r in zip(emids,ratings):
        if r.firstChild!=None:
            result.append((e.firstChild.data,r.firstChild.data))
    return result

#
#
#由于hotornot暂时用不了，所以这里先放下。这部分的内容在书上162~165
#
#

#全局测试函数
if 1:
    print getrandomratings(5)
