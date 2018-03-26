# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 12:32:11 2018

@author: 赵怀菩
"""
import random
import math
import numpy as np
from draw_pic import *

class data_builder(object):
    def __init__(self,min_x_value,max_x_value,length,random_factor=0,commonfactor=1):
        self.xlist=[]
        self.randomlize_xlist=[]
        self.min_x=min_x_value
        self.max_x=max_x_value
        self.length=length
        self.random_factor=random_factor
        self.common=commonfactor
        self.build_array()
        self._build_random_array()
        #
    def build_array(self):
        #build a sin array
        if self.length<240:
            print ('too small array: at least 240')
            return
        a=[x for x in range(self.length)]
        #a is xaxis
        b=self.max_x-self.min_x
        k=b/2
        
        b=[(math.sin(i/12)+1)*k+self.min_x for i in a]
        self.xlist=b
        #b is value in yaxis
        pass
    def _build_random_array(self,array=False,start=0,end=False):
        #start and end of this index
        #random value is expand of the random series
        if self.length<240:
            print ('too small array: at least 240')
            return
        if array==False:
            array=self.xlist
        if end==False:
            end=self.length
            
        temp_array=[]
        if end-start<1:
            return
        rand=np.random.normal(size=end-start)
        for i in range(end-start):
            if abs(rand[i])>0.05:
                #too common ,not changes
                temp=((rand[i]*self.random_factor)+1)*array[start+i]
                temp_array.append(temp)
            else:
                temp_array.append(array[start+i])
        
        #then do the total len change
        randb=np.random.normal(size=end-start)
        now=start
        dx=self.max_x-self.min_x
        for i in range(end-start):
            if abs(randb[i])<1.5:
                pass
            elif i+start>=now:
                #start line change
                blocklength=int(rand[i]*0.6+100)
                blocklength=min(blocklength,end-i)
                blockshift=randb[i]*0.05*dx
                for j in range(blocklength):
                    temp_array[i+j]=temp_array[i+j]+blockshift
                now=now+blocklength
        
        self.randomlize_xlist=temp_array
        return temp_array
    def _add_rare(self,complexity):
        #complexity determind how long the rare array
        rare_array=[]
        for i in range(int(complexity)):
            
            pass
     def _build_sin(self,A,w,fai,length,dx=1/12):
         #f(x)=Asin(wx+fai)
         a=[x for x in range(length)]
         #a is xaxis
         b=[A*(math.sin(i*dx*w+fai)) for i in a]
         return b
         pass
        
        
    
if __name__=='__main__':
    b=data_builder(20,30,600,0.025,1)
    a=[x for x in range(600)]
    draw_pic(b.randomlize_xlist,False,a)
    pass