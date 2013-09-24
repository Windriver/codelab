# -*- coding: utf-8 -*-

#读取博客数据，生成列名、栏名和浮点数据矩阵
def readfile(filename):
    lines=[line for line in file(filename)]

    #读入第一行（都是单词）
    colnames=lines[0].strip().split('\t')[1:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip().split('\t')
        
        #The name of RSS
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])

    print "共读入了 %d 行" % len(lines)
    return rownames,colnames,data

#计算两列表的皮尔逊分值
from math import sqrt

def pearson(v1,v2):
    #求和
    sum1=sum(v1)
    sum2=sum(v2)

    #求平方和
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])

    #求乘积之和
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])

    #计算r（Pearson score），sqrt是求平方根
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
    if den==0:
        return 0

    #在两者完全匹配的情况下r=1.0，在完全不匹配的情况下是0.0
    return 1-num/den

#这个类叫做”聚类“，表示层级树的结点
class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance

#层次聚类函数，以数据矩阵和皮尔逊函数为参数
def hcluster(rows,distance=pearson):
    distances={}
    currentclustid=-1

    #用数据集中的各行来初始化聚类行
    clust=[bicluster(rows[i],id=i) for i in range(len(rows))]

    while len(clust)>1:
        lowestpair=(0,1) #每轮循环开始时的初始值
        closest=distance(clust[0].vec,clust[1].vec)

        #遍历每一个配对，寻找最小距离及其二元组
        for i in range(len(clust)):
            for j in range(i+1,len(clust)):
                #用distances来缓存距离，其键为元组，注意j永远大于i
                if (clust[i].id,clust[j].id) not in distances:
                    distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)

                #通过字典获得两结点间距离
                d=distances[(clust[i].id,clust[j].id)]

                if d<closest:
                    closest=d
                    lowestpair=(i,j)

        #计算聚类i结点和j结点的平均值
        mergevec=[
            (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0
            for i in range(len(clust[0].vec))]

        #建立新的聚类结点
        newcluster=bicluster(mergevec,left=clust[lowestpair[0]],right=clust[lowestpair[1]],
                            distance=closest,id=currentclustid)

        currentclustid-=1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    #此时列表中只剩一个元素
    return clust[0]

#用层级结构打印出聚类结果
import sys
def printclust(clust,labels=None,n=0):
    #打印n个空格实现缩进
    for i in range(n):
        sys.stdout.write(' ')

    if clust.id<0: #负数代表合成结点
        sys.stdout.write('-\n')
    else:  #非负代表叶子结点
        if labels==None:
            print clust.id
        else:
            print labels[clust.id]

    #打印右侧分支和左侧分支
    if clust.left!=None:
        printclust(clust.left,labels=labels,n=n+1)
    if clust.right!=None:
        printclust(clust.right,labels=labels,n=n+1)


#以下代码画出层次聚类的JPG图
from PIL import Image,ImageDraw

#这里的高度是指某节点的所有后代结点的个数
def getheight(clust):
    #是叶子结点，则返回1
    if clust.left==None and clust.right==None:
        return 1

    return getheight(clust.left)+getheight(clust.right)

#这里的深度是指结点的高度
def getdepth(clust):
    if clust.left==None and clust.right==None:
        return 0

    #还要加上该结点的distance值
    return max(getdepth(clust.left),getdepth(clust.right))+clust.distance

#画出树状枝图
def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
    #获取图的高度和宽度
    h=getheight(clust)*20
    w=1200
    depth=getdepth(clust)

    #由于宽度是固定的，所以我们要对距离值进行相应的调整
    scaling=float(w-150)/depth

    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    draw.line((0,h/2,10,h/2),fill=(255,0,0))

    #draw the first node
    drawnode(draw,clust,10,(h/2),scaling,labels)
    img.save(jpeg,'JPEG')

#接受一个聚类及其位置作为输入参数
def drawnode(draw,clust,x,y,scaling,labels):
    if clust.id<0:
        h1=getheight(clust.left)*20
        h2=getheight(clust.right)*20
        top=y-(h1+h2)/2
        bottom=y+(h1+h2)/2
        #横线的长度
        ll=clust.distance*scaling

        #画出聚类到其两个子节点的垂直线
        draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))

        #画出连接器左右结点的水平线
        draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))
        draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))

        #递归绘制左右结点
        drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
        drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
    else:
        #如果是叶子结点，则绘制标签上的博客名
        draw.text((x+5,y-7),labels[clust.id],fill=(0,0,0))

#矩阵转置函数，以实现按列（单词）聚类
def rotatematrix(data):
    newdata=[]
    for i in range(len(data[0])): #len(data[0])为列的长度
        newrow=[data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata

#
#K-均值聚类
#
import random

def kcluster(rows,distance=pearson,k=4):
    #ranges是由元组构成的列表，元组值为每个单词的最大频度和最小频度
    ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows]))
            for i in range(len(rows[0]))]

    #随机创建k个中心点，每个中心点的维数和参与聚类的特征单词数相同
    cluster=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0]
             for i in range(len(rows[0]))] for j in range(k)]

    #K-均值聚类的迭代开始
    lastmatches=None
    for t in range(100):
        print 'Iteration %d' % t
        bestmatches=[[] for i in range(k)]

        #外层循环的j代表行号，内层循环的i代表聚类id
        for j in range(len(rows)):
            row=rows[j]
            bestmatch=0
            #循环k轮，更新bestmatch值，使其真正best
            for i in range(k):
                d=distance(cluster[i],row)
                if d<distance(cluster[bestmatch],row):
                    bestmatch=i
            #将j加入到第bestmatch个聚类中
            bestmatches[bestmatch].append(j)

        #如果两轮迭代结果相同，则过程结束
        if bestmatches==lastmatches:
            break
        lastmatches=bestmatches

        #重新计算每个聚类的中心点
        for i in range(k):
            avgs=[0.0]*len(rows[0])
            if len(bestmatches[i])>0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m]+=rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                cluster[i]=avgs
                
    print "第 %d 轮时结束" % t
    return bestmatches

#Chapter 3.7 : 针对偏好的聚类
#由于zebo网站已经无法访问，故直接从kiwitobes网站下载现成的数据
#

#本次聚类，因为列表中的数据都是0或1（表示无或有），故用Tanimoto来衡量列表的距离
def tanimoto(v1,v2):
    c1,c2,shr=0,0,0

    for i in range(len(v1)):
        if v1[i]!=0:
            c1+=1
        if v2[i]!=0:
            c2+=1
        if v1[i]!=0 and v2[i]!=0:
            shr+=1 #求交集中元素个数

    return 1.0-(float(shr)/(c1+c2-shr))

#Chapter 3.8 : 以二维形式展现数据
#多维缩放技术就是为多维数据集找寻二维表示形式
#

#使用了“拉力算法”
def scaledown(data,distance=pearson,rate=0.01):
    n=len(data)

    #reallist表示每对数据项之间的真实距离
    reallist=[[distance(data[i],data[j]) for j in range(n)]
              for i in range(n)]

    outersum=0.0

    #随机初始化结点在二维空间的初始位置
    loc=[[random.random(),random.random()] for i in range(n)]
    #fakelist是当前的实际距离
    fakelist=[[0.0 for j in range(n)]
              for i in range(n)]

    lasterror=None
    for m in range(0,1000):
        #计算当前的实际距离
        for i in range(n):
            for j in range(n):
                fakelist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2)
                                         for x in range(len(loc[i]))]))

        #每轮节点应该移动的x，y轴距离
        grad=[[0.0,0.0] for i in range(n)]

        totalerror=0
        for k in range(n):
            for j in range(n):
                if j==k:
                    continue
                #误差值等于目标真实距离与当前距离之间的差值的百分比
                #这里的公式还不懂原理(根据网上的帖子，为分母加了1)
                errorterm=(fakelist[j][k]-reallist[j][k])/(reallist[j][k]+1)

                grad[k][0]+=((loc[k][0]-loc[j][0])/fakelist[j][k])*errorterm
                grad[k][1]+=((loc[k][1]-loc[j][1])/fakelist[j][k])*errorterm

                #记录累积的误差值
                totalerror+=abs(errorterm)
        print totalerror

        #如果移动节点之后情况变得更糟，则不移动，并结束程序
        if lasterror and totalerror>lasterror:
            break
        lasterror=totalerror

        #根据rate参数和grad之积来移动节点
        for k in range(n):
            loc[k][0]-=rate*grad[k][0]
            loc[k][1]-=rate*grad[k][1]

    return loc

#根据坐标值，在图上的响应位置绘制出所有的标签
def draw2d(data,labels,jpeg='mds2d.jpg'):
    img=Image.new('RGB',(2000,2000),(255,255,255))
    draw=ImageDraw.Draw(img)
    for i in range(len(data)):
        x=(data[i][0]+0.5)*1000
        y=(data[i][1]+0.5)*1000
        draw.text((x,y),labels[i],(0,0,0))
    img.save(jpeg,'JPEG')
    
                
                

#全局测试代码
#blognames,words,data=readfile('blogdata.txt')
#print "bolg number is %d ,word number is %d" % (len(blognames),len(words))

#
#按博客进行聚类
#clust=hcluster(data)
#printclust(clust,labels=blognames)
#drawdendrogram(clust,blognames,jpeg='bolgclust.jpg')

#
#按单词进行列聚类
#rdata=rotatematrix(data)
#wordclust=hcluster(rdata)
#drawdendrogram(wordclust,labels=words,jpeg='wordclust.jpg')

#kclust=kcluster(data,k=6)
#print "Clust 0:"
#print [blognames[r] for r in kclust[0]]
#print "Clust 1:"
#print [blognames[r] for r in kclust[1]]
#print "Clust 2:"
#print [blognames[r] for r in kclust[2]]
#print "Clust 3:"
#print [blognames[r] for r in kclust[3]]
#print "Clust 4:"
#print [blognames[r] for r in kclust[4]]
#print "Clust 5:"
#print [blognames[r] for r in kclust[5]]#

#
#对zebo网站的数据进行聚类
#wants,peoole,data=readfile('zebo.txt')
#clust=hcluster(data,distance=tanimoto)
#drawdendrogram(clust,wants,jpeg='zeboclust.jpg')

#
#以二维形式展现数据
blognames,words,data=readfile('blogdata.txt')
coords=scaledown(data)
draw2d(coords,blognames)
