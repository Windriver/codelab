# -*- coding: utf-8 -*-

import math

#
#网络可视化：人们的社交关系清晰都表示出来
#

people=['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']

links=[('Augustus', 'Willy'),
       ('Mike', 'Joe'),
       ('Miranda', 'Mike'),
       ('Violet', 'Augustus'),
       ('Miranda', 'Willy'),
       ('Charlie', 'Mike'),
       ('Veruca', 'Joe'),
       ('Miranda', 'Augustus'),
       ('Willy', 'Augustus'),
       ('Joe', 'Charlie'),
       ('Veruca', 'Augustus'),
       ('Miranda', 'Joe')]


#借助质点弹簧算法，各节点彼此向对方施以推力并试图分离，而有连接的两个关联结点则还有彼此试图靠近的力
#但是该算法无法避免交叉线，所以下面的成本函数是计算彼此的交叉线数，后面还要加上节点过于靠近的惩罚值

def crosscount(v):
    #将数字序列转换成person：(x,y)的字典
    loc=dict([(people[i],(v[2*i],v[2*i+1])) for i in range(len(people))])
    total=0

    #通过links来遍历每一对连线
    for i in range(len(links)):
        for j in range(i+1,len(links)):
            #通过i，j获得4个坐标
            (x1,y1),(x2,y2)=loc[links[i][0]],loc[links[i][1]]
            (x3,y3),(x4,y4)=loc[links[j][0]],loc[links[j][1]]
            #print loc[links[i][0]],loc[links[i][1]]
            #print loc[links[j][0]],loc[links[j][1]]
            den=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
            #print den
            #den=0表示两线平行
            if den==0:
                
                continue

            #否则，ua与ub就是两条交叉线的分数值。这里要转化成float，否则ua，ub为整数，下面的条件永远不成立
            ua=float((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/den
            ub=float((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/den
            #print ua, ub
            #如果两条线的分数值介于0和1之间，则两线彼此交叉
            if ua>0 and ua<1 and ub>0 and ub<1:
                #print total
                total+=1

    for i in range(len(people)):
        for j in range(len(people)):
            #获得两点的位置
            (x1,y1),(x2,y2)=loc[people[i]],loc[people[j]]

            #计算两点的间距
            dist=math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
            #对间距小于50像素的结点进行惩罚
            if dist<50:
                total+=(1.0-(dist/50.0))
    
    #print total
    return total


#这里的domain表示了点在图上坐标值的范围，这种题解的形式跟本题息息相关
domain=[(10,370)]*(len(people)*2)


#绘制网格
from PIL import Image,ImageDraw

def drawnetwork(sol):
    #建立image对象
    img=Image.new('RGB',(400,400),(255,255,255))
    draw=ImageDraw.Draw(img)

    pos=dict([(people[i],(sol[i*2],sol[i*2+1])) for i in range(len(people))])

    #绘制连线
    for a,b in links:
        draw.line((pos[a],pos[b]),fill=(255,0,0))

    #绘制结点信息
    for n,p in pos.items():
        draw.text(p,n,(0,0,0))

    #只是显示图形，而不存储
    img.show()

#全局测试代码
if 1:
    import optimization
    sol=optimization.randomoptimize(domain,crosscount)
    print sol
    print crosscount(sol)
    drawnetwork(sol)
