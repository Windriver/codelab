# -*- coding: utf-8 -*-

import time
import urllib2
import xml.dom.minidom

kayakkey='YOURKEYHERE'

def getkayaksession():
    #构造URL以开启一个会话
    url='http://www.kayak.com/k/ident/apisession?token=%s&version=1' % kayakkey

    #解析返回的XML
    doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())
    print urllib2.urlopen(url).read()
    #找到<sid>xxxxxxxxxx</sid>标签
    sid=doc.getElementsByTagName('sid')[0].firstChild.data
    return sid

#貌似Kayak的API已经停用了
#下面是官方的申明：
#
#Kayak Search API is no longer supported
#
#Because of costly misuse of the search API, KAYAK no longer can support it. Sorry.

#全局测试代码一
if 1:
    print getkayaksession()
