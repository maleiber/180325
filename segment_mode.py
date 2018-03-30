# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 21:09:56 2018

@author: 赵怀菩
"""
from customize_tool import *
import draw_pic
import data_builder

class segment_mode(object):
    def __init__(self,minl,maxl,data_array):
        self.min_len=minl
        self.max_len=maxl
        self.dataseq=data_array
        self.data_sign=[]
        self.sub_seq_information=[]
        self.sub_dict={}
        self.color_value=[]
        
        self._blurry()
        self._standardlize()
        self._bottom_up_merge()
        pass
    def _blurry(self):
        
        new_seq=[   #int(
                        1/7*self.dataseq[max(i-3,0)]+
                        1/7*self.dataseq[max(i-2,0)]+
                        1/7*self.dataseq[max(i-1,0)]+
                        1/7*self.dataseq[i]+
                        1/7*self.dataseq[min(i+1,len(self.dataseq)-1)]
                        +1/7*self.dataseq[min(i+2,len(self.dataseq)-1)]
                        +1/7*self.dataseq[min(i+3,len(self.dataseq)-1)]
                    #)
                    for i in range(len(self.dataseq))
                ]
        self.dataseq=new_seq
            
        pass
    def _standardlize(self):
        self.dataseq=Z_ScoreNormalization(self.dataseq)
        pass
    def __build_origin_segment(self):
        prev=self.dataseq[0]

        #self.data_sign.append(prev)
        for i in range(len(self.dataseq)-1):
            now=self.dataseq[i]
            self.data_sign.append(now-prev)
            prev=now
        #finished dx
        a=[i for i in range(len(self.data_sign))]
        draw_pic.draw_pic(self.data_sign,False,a)
        pass
    def _bottom_up_merge(self):
        self.__build_origin_segment()
        
        pass
    
    def slide_cos_search(self):
        
        #get all sub
        w=self.min_len
        while w<self.max_len:
            print('w',w)
            for i in range(len(self.data_sign)):
                start=i
                end=i+w
                
                if end+1>=len(self.data_sign):
                    #goal sub exceed
                    break
                sub_seq=self.data_sign[start:end]
                sub_key=hash(tuple(sub_seq))
                self.sub_dict[sub_key]=[start,end]
            #the goal subseq is after now, before has been found.
            w=w+1
            pass
        self.sub_cos={}
        #calulate cos of all sub
        for p1 in self.sub_dict:
            s1,e1=self.sub_dict[p1]
            for p2 in self.sub_dict.items():
                s2,e2=self.sub_dict[p2]
                if s2>e1 or s1>e2:
                    sub1=self.data_sign[s1:e1]
                    sub2=self.data_sign[s2:e2]
                    value=cos(sub1,sub2)
                    self.sub_cos[(s1,e1,s2,e2)]=value
        pass
    
    def segment_mode(self):
        #bottom_up fitting
        #fitting the raw and signalize it.
        #  not only can reduce total length but also take out noise
        #  extremum lost
        self.dataseq
    
    def density_clu(self):
        
        
        
        pass
    pass



if __name__=='__main__':
    b=data_builder.data_builder(20,30,1200,0.025,1)
    a=[x for x in range(1200)]
    draw_pic.draw_pic( b.randomlize_xlist,False,a)
    
    b.add_rare(100,80)
    b.add_rare(100,80)
    b.insert_rare_in_rlist()
    c=segment_mode(70,100, b.randomlize_xlist)
    pass