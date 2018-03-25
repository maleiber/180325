# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 08:18:32 2018

@author: 赵怀菩
"""
from draw_pic import *
from diskwalk import *



if __name__ == '__main__':
    sitelist=[]
    x=[1,2,3,5]
    y=[11,12,13,24]
    xcolor=[20,20,232,223]
    a=draw_pic(x)
    b=draw_pic(x,xcolor)
    c=draw_pic(x,xcolor,y)
    for file in diskwalk("D:/zhp_workspace/35site").paths():
        print(file)
        filename=file
        #sitelist.append(timeseq(filename))
                