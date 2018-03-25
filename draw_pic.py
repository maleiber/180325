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
    def __init__(self,xarray,xcolor=False,yarray=False):
        print (xarray,xcolor,yarray)
        fig,ax = plt.subplots()
        #fig.set_size_inches(108.5, 10.5)
        ax.grid(True)
        a=xarray
        cm = plt.cm.get_cmap('RdYlBu')
        if xcolor==False:
            z=[250 for i in xarray]
        else:
            z=xcolor
        if yarray==False:
            b=[i for i in range(len(xarray))]
        else:
            b=yarray
        sc = plt.scatter(b, a, c=z, vmin=0, vmax=256, s=35, cmap=cm)
        ax.plot(b,a)
        plt.colorbar(sc)
        plt.show()
        pass
    
if __name__ == '__main__':
    a=[x for x in range(100)]
    #a is xaxis
    b=[math.sin(i/10) for i in a]
    #b is value in yaxis
    z=[random.randint(0,255) for i in a]
    #z is color of each point
    cm = plt.cm.get_cmap('RdYlBu')
    
    
    fig.set_size_inches(108.5, 10.5)
    fig,ax = plt.subplots()
    
    sc = plt.scatter(a, b, c=z, vmin=0, vmax=256, s=35, cmap=cm)  
    plt.colorbar(sc)  
    plt.show()
        