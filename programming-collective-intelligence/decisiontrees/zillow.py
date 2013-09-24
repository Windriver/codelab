# -*- coding: utf-8 -*-

import xml.dom.minidom
import urllib2

zwskey="X1-ZWZ1chwxis15aj_9skq6"

def getaddressdata(address,city):
    #用加号替代空格填充单词
    escad=address.replace(' ','+')

    #构造URL
    url="http://www.zillow.com/webservice/GetDeepSearchResults.htm?"
    url+="zws-id=%s&address=%s&citystatezip=%s" % (zwskey,escad,city)

    #解析XML形式的返回结果
    doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())
    code=doc.getElementsByTagName('code')[0].firstChild.data
    
    #状态码为0代表操作成功，否则代表有错误发生
    #这里书上代码有错误，因为从doc中获得的都是unicode，不能直接和int比较
    if int(code)!=0:
        print type(code)
        print "Error"
        return None

    #提取有关该房产的信息
    try:
        zipcode=doc.getElementsByTagName('zipcode')[0].firstChild.data
        use=doc.getElementsByTagName('useCode')[0].firstChild.data
        year=doc.getElementsByTagName('yearBuilt')[0].firstChild.data
        bath=doc.getElementsByTagName('bathrooms')[0].firstChild.data
        bed=doc.getElementsByTagName('bedrooms')[0].firstChild.data
        rooms=doc.getElementsByTagName('totalRooms')[0].firstChild.data
        price=doc.getElementsByTagName('amount')[0].firstChild.data
    except:
        return None
    print zipcode,use,year,bath,bed,rooms,price

    return (zipcode,use,int(year),float(bath),int(bed),int(rooms),price)

def getpricelist():
    ll=[]
    for line in file('addresslist.txt'):
        data=getaddressdata(line.strip(),'Cambrige,MA')
        #这里需要加个判断语句，因为list会蛋疼地将None加入，使求方差时出错
        if data!=None:
            ll.append(data)
    return ll


#
#

#
#

#全局测试代码一
if 1:
    housedata=getpricelist()
    import treepredict
    housetree=treepredict.buildtree(housedata,scoref=treepredict.variance)
    treepredict.drawtree(housetree)
