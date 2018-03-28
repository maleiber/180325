# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 18:51:49 2018

@author: 赵怀菩
"""
import bm_test
import numpy as np
import draw_pic
import data_builder

class bm_analyze(object):
    def __init__(self,minl,maxl,data_array):
        self.min_len=minl
        self.max_len=maxl
        self.dataseq=data_array
        self.sub_seq_information=[]
        self.sub_dict={}
        self.color_value=[]
        self._blurry()
        pass
    def _blurry(self):
        
        new_seq=[   int(
                        1/5*self.dataseq[max(i-2,0)]+
                        1/5*self.dataseq[max(i-1,0)]+
                        1/5*self.dataseq[i]+
                        1/5*self.dataseq[min(i+1,len(self.dataseq)-1)]+
                        1/5*self.dataseq[min(i+2,len(self.dataseq)-1)]
                    )
                    for i in range(len(self.dataseq))
                ]
        self.dataseq=new_seq
            
        pass
    def bm_search(self):
        #origin version
        
        
        for sub_len in range(self.min_len,self.max_len+1):
            print ('now sublen:',sub_len)
            for i in range(len(self.dataseq)):
            #i is p
                #len of subseq is [min,max]
                
                sub_end=i+sub_len
                if sub_end>=len(self.dataseq):
                    #goal sub exceed
                    break
                sub_seq=self.dataseq[i:sub_end]
                if self.sub_dict.get(hash(tuple(sub_seq)))!=True:
                    #not search this seq yet
                    pattern_array=bm_test.BoyerMooreHorspool(sub_seq,self.dataseq)
                    
                    if(len(pattern_array))>1:
                        print ('effective sub seq at:',i)
                        #input()
                    #[time(or key value) position]
                    self.sub_seq_information.append([self._value_sub_seq_in_rare(pattern_array,sub_seq),pattern_array,sub_len])
                    self.sub_dict[hash(tuple(sub_seq))]=True
        #search finished. then sort by value
        sorted(self.sub_seq_information,key=lambda x:x[0])
        #normalize the value as value
        color_value=[x[0] for x in self.sub_seq_information]
        color_value=Z_ScoreNormalization(color_value,np.average(color_value),np.std(color_value))
        color_value=[int(v*60) for v in color_value]
        print (color_value)
        for i in range(len(self.sub_seq_information)):
            self.sub_seq_information[i][0]=color_value[i]
            
        self._fill_color_value()
        pass
    
    def _value_sub_seq_in_rare(self,pattern_array,sub):
        #value by complexity, length, and appearence time
        complexity=np.std(sub)
        leng=len(sub)
        appearence_t=len(pattern_array)
        _value=complexity*leng/(appearence_t)
        return _value
    
    def _fill_color_value(self):
        self.color_value=[10 for x in self.dataseq]
        for i in range(len(self.sub_seq_information)):
            value=self.sub_seq_information[i][0]
#            if value < 0.75:
#                continue
            position=self.sub_seq_information[i][1]
            temp_len=self.sub_seq_information[i][2]
            for p in position:
                for j in range(temp_len):
                    self.color_value[p+j]=max(value,abs(self.color_value[p+j]))
            
        pass
    pass
def Z_ScoreNormalization(x,mu,sigma):  
    x = (x - mu) / sigma;  
    return x;  

if __name__=='__main__':
    
    b=data_builder.data_builder(20,30,1000,0.025,1)
    a=[x for x in range(1000)]
    draw_pic.draw_pic([int(x) for x in b.randomlize_xlist],False,a)
    
    b.add_rare(100,80)
    b.add_rare(100,90)
    b.insert_rare_in_rlist()
    c=bm_analyze(60,100,[int(x) for x in b.randomlize_xlist])
    c.bm_search()

    a=[x for x in range(len(b.randomlize_xlist))]
    draw_pic.draw_pic([int(x) for x in b.randomlize_xlist],False,a)
    print ('color value',c.color_value)
    
    draw_pic.draw_pic(c.dataseq,c.color_value,a)
    pass