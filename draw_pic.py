# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 08:36:30 2018

@author: 赵怀菩
"""
import pandas as pd
import matplotlib.pyplot as plt

class draw_pic(object):
    def __init__(self,xarray,xcolor=False,yarray=False):
        print (xarray,xcolor,yarray)
        fig,ax = plt.subplots()
        fig.set_size_inches(108.5, 10.5)
        ax.grid(True)
        if yarray==False:
            ax.plot(xarray)
        else:
            ax.plot(yarray,xarray)
        if xcolor==False:
            pass
        plt.show()
        pass