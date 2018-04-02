# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 08:36:30 2018

@author: 赵怀菩
"""
import pandas as pd
import matplotlib.pyplot as plt
import random
import math

class draw_pic(object):
    def __init__(self,yarray,xcolor=False,xarray=False,draw_line=True,save_name=''):
        #value of yarray is necessary
        #print (yarray,xcolor,xarray)
        fig,ax = plt.subplots()
        fig.set_size_inches(48.5, 10.5)
        ax.grid(True)
        a=yarray
        v_min=0
        v_max=250
        #cm = plt.cm.get_cmap('RdYlBu')
        cm = plt.cm.get_cmap('brg')
        if type(xcolor)==bool:
            z=[250 for i in yarray]
        else:
            z=xcolor
            v_min=min(z)
            v_max=max(z)
        
        if type(xarray)==bool :
            b=[i for i in range(len(yarray))]
        else:
            b=xarray
        sc = plt.scatter(b, a, c=z, vmin=v_min, vmax=v_max, s=35, cmap=cm)
        if draw_line==True:
            ax.plot(b,a,alpha=0.2)
        plt.colorbar(sc)
        if len(save_name)>0:
            save_name=save_name+'.png'
            plt.savefig(save_name, dpi=100)
        plt.show()
        pass

class draw_sca(object):
    def __init__(self,x,y,alpha=False):
        fig,ax = plt.subplots()
        fig.set_size_inches(12,12)
        ax.grid(True)
        a=x
        b=y
        cm = plt.cm.get_cmap('RdYlBu')
        z=[1 for i in range(len(x))]
        if alpha==False:
            pass
        else:
            pass
        
        
        sc = plt.scatter(b, a, c=z,alpha=0.3,vmin=0, vmax=1256, s=35, cmap=cm)
        plt.colorbar(sc)
        plt.show()
        pass
    pass
if __name__ == '__main__':
    a=[x for x in range(500)]
    #a is xaxis
    b=[math.sin(i/12) for i in a]
    #b is value in yaxis
    z=[random.randint(0,255) for i in a]
    #z is color of each point
    sc = plt.scatter(a, b, c=z, vmin=0, vmax=256, s=35, cmap=cm)
    x=[1,2,3,5]
    y=[11,12,13,24]
    xcolor=[20,20,232,223]
    draw_pic(x)
    draw_pic(x,xcolor)
    draw_pic(x,xcolor,y)
    draw_pic(x,xcolor,y,False)
        