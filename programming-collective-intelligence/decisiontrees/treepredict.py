# -*- coding: utf-8 -*-

import re

#
#chapter 7: 决策树建模
#


#加载数据文件，生成数据矩阵，但是由于split('\t')会导致分割和还留存\t，
#故还需进一步用正则表达式的re.sub(pattern, repl, string, count)来去掉\t

my_data=[line.split('\t') for line in file('decision_tree_example.txt')]
for i in range(len(my_data)):
    for j in range(len(my_data[i])):
        my_data[i][j]=re.sub(r'\n','',my_data[i][j])

#上面的数据是从kiwitobes官网上下载的，跟书上给的不一样，导致建立的决策树跟书上的不大一样
#在这里卡了好久啊（半天多）！！！
my_data=[['slashdot','USA','yes',18,'None'],
         ['google','France','yes',23,'Premium'],
         ['digg','USA','yes',24,'Basic'],
         ['kiwitobes','France','yes',23,'Basic'],
         ['google','UK','no',21,'Premium'],
         ['(direct)','New Zealand','no',12,'None'],
         ['(direct)','UK','no',21,'Basic'],
         ['google','USA','no',24,'Premium'],
         ['slashdot','France','yes',19,'None'],
         ['digg','USA','no',18,'None'],
         ['google','UK','no',18,'None'],
         ['kiwitobes','UK','no',19,'None'],
         ['digg','New Zealand','yes',12,'Basic'],
         ['slashdot','UK','no',21,'None'],
         ['google','UK','yes',18,'Basic'],
         ['kiwitobes','France','yes',19,'Basic']]


#决策树上的结点，col为待检测的列的索引值，value对应了使结果为true，当前列必须匹配的值
class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb
        self.fb=fb

#
#chapter 7.3: 对树进行训练
#本章使用了CART（即分类回归树）的算法，构造回归树。
#函数divideset在作用是根据列表中的某一栏的数据将列表拆分为两个数据集
#
def divideset(rows,column,value):
    #用lambda定义一个函数赋值给split_function
    split_function=None
    #根据value是数值型的还是名词性的数据执行不同的判断策略
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value

    #拆分出两个数据集
    set1=[row for row in rows if split_function(row)]
    set2=[row for row in rows if not split_function(row)]
    return (set1,set2)

#对行中不同的数据进行计数，其他函数（如基尼不纯度和墒）利用该函数来计算数据集合的混杂程度
def uniquecounts(rows):
    results={}
    for row in rows:
        r=row[len(row)-1]
        if r not in results:
            results[r]=0
        results[r]+=1
    return results

#基尼不纯度：将不同结果的概率两两相乘在求和，这样就得到了rows中的某行数据被分配到错误结果的概率
def giniimpurity(rows):
    total=len(rows)
    counts=uniquecounts(rows)
    imp=0
    for k1 in counts:
        for k2 in counts:
            p1=float(counts[k1])/total
            if k2==k1:
                continue
            p2=float(counts[k2])/total
            imp+=p1*p2
    return imp

#熵代表集合的无序程度，我们将数据拆分成两个新的组，其目的就是要降低熵
def entropy(rows):
    from math import log
    log2=lambda x:log(x)/log(2)
    results=uniquecounts(rows)
    #开始计算熵
    ent=0.0
    for r in results.keys():
        p=float(results[r])/len(rows)
        ent-=p*log2(p)
    return ent

#递归方式构造决策树，传入熵函数或者基尼不纯度函数
def buildtree(rows,scoref=entropy):
    if len(rows)==0:
        return decisionnode()

    current_score=scoref(rows)

    #记录最佳拆分条件的3个变量
    best_gain=0.0
    best_criteria=None
    best_sets=None

    column_count=len(rows[0])-1
    #遍历二维矩阵，找出最佳的col与value
    for col in range(0,column_count):
        #在当前列中生成一个由不同值(value)构成的序列（即去重）
        column_values={}
        for row in rows:
            column_values[row[col]]=1
        #根据value构成的字典中的每个值，尝试对数据集进行拆分
        for value in column_values.keys():
            #print value
            (set1,set2)=divideset(rows,col,value)

            #计算信息增益
            p=float(len(set1))/len(rows)
            #print p
            gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
            #print 'gain'+str(gain)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain=gain
                best_criteria=(col,value)
                best_sets=(set1,set2)
    #创建子分支
    if best_gain>0:
        #print 'best_gain'+str(best_gain)
        trueBranch=buildtree(best_sets[0])
        falseBranch=buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0],value=best_criteria[1],
                            tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))

#
#chapter 7.6: 决策树的显示
#

#简单的显示方法
def printtree(tree,indent=' '):
    #这是一个叶子节点吗？
    if tree.results!=None:
        print str(tree.results)
    else:
        #打印判断条件
        print str(tree.col)+':'+str(tree.value)+'? '

        #打印分支
        print indent+'T->',
        printtree(tree.tb,indent+' ')
        print indent+'F->',
        printtree(tree.fb,indent+' ')

#图形显示方式（使用PIL绘制）
        
#求一个给定节点的所有子节点所占用的总宽度
def getwidth(tree):
    if tree.tb==None and tree.fb==None:
        return 1 #如果一个节点无子分支，则其对应的宽度为1
    return getwidth(tree.tb)+getwidth(tree.fb)

#求一个给定节点所要达到的深度值(使其子节点拥有足够的深度值）
def getdepth(tree):
    if tree.tb==None and tree.fb==None:
        return 0
    return max(getdepth(tree.tb),getdepth(tree.fb))+1 #等于其最长子分支的总深度值加1

#绘图
from PIL import Image,ImageDraw

def drawtree(tree,jpeg='tree.jpeg'):
    w=getwidth(tree)*120
    h=getdepth(tree)*100+120 #每层占100个像素

    #设置好画布（canvas）
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)

    drawnode(draw,tree,w/2,20) #在坐标点(w/2,20)处绘制根节点，再递归绘制完整棵树
    img.save(jpeg,'JPEG')

def drawnode(draw,tree,x,y):
    #非叶子结点
    if tree.results==None:
        #得到其两个分支的宽度
        w1=getwidth(tree.fb)*100
        w2=getwidth(tree.tb)*100

        #确定此结点及其所有后代的占用总宽度的起始x值和结束x值
        left=x-(w1+w2)/2
        right=x+(w1+w2)/2

        #绘制判断条件（注意x，y都减了20）
        draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))

        #绘制到两个分支的连线
        draw.line((x,y,left+w1/2,y+100-15),fill=(255,0,0))
        draw.line((x,y,right-w2/2,y+100-15),fill=(255,0,0))

        #绘制分支的节点（先画假分支，再画真分支）
        drawnode(draw,tree.fb,left+w1/2,y+100)
        drawnode(draw,tree.tb,right-w2/2,y+100)
    #叶子节点
    else:
        txt=' \n'.join(['%s:%d' % v for v in tree.results.items()])
        draw.text((x-20,y-10),txt,(0,0,0))
    
#
#Chapter 7.7: 对新的观测数据进行分类
#接受新的观测数据作为参数
#
def classify(observation,tree):
    if tree.results!=None:
        return tree.results
    else:
        v=observation[tree.col] #取出某一栏的观测值
        branch=None
        if isinstance(v,int) or isinstance(v,float):
            if v>tree.value:
                branch=tree.tb
            else:
                branch=tree.fb
        else:
            if v==tree.value:
                branch=tree.tb
            else:
                branch=tree.fb
        #到下一层，递归判断
        return classify(observation,branch)

#
#Chapter 7.8: 决策树的剪枝
#训练出的决策树可能会“过度拟合”，即过于针对训练数据，导致得出的答案比实际情况更具有特殊性，故有剪枝操作
#

#剪枝策略是：先构造好决策树，再从底向上尝试消除多余的节点，防止错剪上层的枝干
def prune(tree,mingain):
    #如果分支不是叶节点，则对其进行剪枝操作
    if tree.tb.results==None:
        prune(tree.tb,mingain)
    if tree.fb.results==None:
        prune(tree.fb,mingain)

    #当tree的tb和fb分支剪枝完后变成叶子节点或者它们本身就是叶子节点，则向下执行
    if tree.tb.results!=None and tree.fb.results!=None:
        #构造合并的数据集，这里的计算方式有点疑惑
        tb,fb=[],[]
        for v,c in tree.tb.results.items():
            tb+=[[v]]*c #没见过这种Python语法
        for v,c in tree.fb.results.items():
            fb+=[[v]]*c #没见过这种Python语法

        #求熵的减少，这里的计算方式有点疑惑
        delta=entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)
        if delta<mingain:
            #合并分支
            tree.tb,tree.fb=None,None
            tree.results=uniquecounts(tb+fb)

#
#Chapter 7.9: 处理缺失的数据
#

def mdclassify(observation,tree):
    if tree.results!=None:
        return tree.results
    else:
        v=observation[tree.col]
        #print v
        #缺失了此处的数据，则tb和fb分支都要走
        if v==None:
            tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
            tcount=sum(tr.values())
            fcount=sum(fr.values())
            tw=float(tcount)/(tcount+fcount)
            fw=float(fcount)/(tcount+fcount)
            print "tw="+str(tw)
            result={}
            for k,v in tr.items():
                result[k]=v*tw
            for k,v in fr.items():
                if k not in result:
                    result[k]=0
                result[k]+=v*fw
            return result
        else:
            #有数据，执行普通的判断
            if isinstance(v,int) or isinstance(v,float):
                if v>=tree.value:
                    branch=tree.tb
                else:
                    branch=tree.fb
            else:
                if v==tree.value: #debug时发现是由于这里写成tree.tb了（通过print发现的），真实闻者足戒啊！！
                    #print tree.value 
                    branch=tree.tb
                else:
                    branch=tree.fb
            return mdclassify(observation,branch)

#
#Chapter 7.10,11,12: 处理数值型的数据，对住房价格进行建模，对“热度”进行建模
#使用发差作为评价函数来取代熵或者基尼不纯度

def variance(rows):
    if len(rows)==0:
        return 0
    data=[float(row[len(row)-1]) for row in rows]
    mean=sum(data)/len(data) #使用len(data)而不是len(rows)
    #下面就是方差的计算公式
    variance=sum([(d-mean)**2 for d in data])/len(data) 
    return variance


#全局测试代码一
if 0:
    #print giniimpurity(my_data)
    #print entropy(my_data)
    tree=buildtree(my_data) #构造决策树
    #printtree(tree)
    #drawtree(tree,jpeg='treeview.jpg')
    print classify(['(direct)','USA','yes',5],tree) #新的观测数据进行分类

#全局测试代码二：
if 0:
    tree=buildtree(my_data)
    prune(tree,0.1)
    prune(tree,1.0) #剪枝
    drawtree(tree,jpeg='treeview.jpg')
    print mdclassify(['google',None,'yes',None],tree) #处理缺失的数据
    print mdclassify(['google','France',None,None],tree)
    
