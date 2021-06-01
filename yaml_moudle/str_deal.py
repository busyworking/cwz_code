# -*- coding: utf-8 -*-#
# Author: chenwenzhi
# Date: 2021/2/24


import copy
a=[1,2,3,4,5,['a','b']]
#原始对象
b=a#赋值，传对象的引用
c=copy.copy(a)#对象拷贝，浅拷贝
d=copy.deepcopy(a)#对象拷贝，深拷贝
print "a=",a,"    id(a)=",id(a),"id(a[5])=",id(a[5])
print "b=",b,"    id(b)=",id(b),"id(b[5])=",id(b[5])
print "c=",c,"    id(c)=",id(c),"id(c[5])=",id(c[5])
print "d=",d,"    id(d)=",id(d),"id(d[5])=",id(d[5])


a.append(6)#修改对象a
a[5].append('c')#修改对象a中的['a','b']数组对象
print "a=",a,"    id(a)=",id(a),"id(a[5])=",id(a[5])
print "b=",b,"    id(b)=",id(b),"id(b[5])=",id(b[5])
print "c=",c,"    id(c)=",id(c),"id(c[5])=",id(c[5])
print "d=",d,"    id(d)=",id(d),"id(d[5])=",id(d[5])

