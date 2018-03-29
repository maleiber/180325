# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 18:51:49 2018

@author: 赵怀菩
"""
import bm_test
import numpy as np
import draw_pic
import data_builder
import math
class bm_analyze(object):
    def __init__(self,minl,maxl,data_array):
        self.min_len=minl
        self.max_len=maxl
        self.dataseq=data_array
        self.data_sign=[]
        self.sub_seq_information=[]
        self.sub_dict={}
        self.color_value=[]
        
        self._blurry()
        self._signallize()
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
    def _signallize(self):
        prev=self.dataseq[0]

        #self.data_sign.append(prev)
        for i in range(len(self.dataseq)-1):
            now=self.dataseq[i]
            self.data_sign.append(now-prev)
            prev=now
        #finished dx
        #normalize

        
        aver=np.average(self.data_sign)
        std=np.std(self.data_sign)
        
        #self.data_sign=Z_ScoreNormalization(self.data_sign,np.average(self.data_sign),np.std(self.data_sign))
        #dont know why the first value is wrong
        tempsign = [(x - aver) / std for x in self.data_sign]; 
        self.data_sign=tempsign
        #self.data_sign=self.data_sign[1:]
        #print ('len of datasign',len(self.data_sign) )
        a=[i for i in range(len(self.dataseq))]
        #draw_pic.draw_pic(self.dataseq,False,a)
        
        
        #devide gradient
        glevel=21
        min_v=min(self.data_sign)
        max_v=max(self.data_sign)
        value_per_g=(max_v-min_v)/glevel
        #print ('data_sign:',self.data_sign)
        #print ('value per geadint:',value_per_g,'min:',min_v,'max_v',max_v)
        #assign glevel
        new_sign=[]
        for i in range(len(self.data_sign)):
            new_sign.append(int(round((self.data_sign[i]-min_v)/value_per_g)))
        self.data_sign=new_sign
        #
        #self.data_sign[0]=(np.average(self.data_sign)-min_v)/value_per_g
        #print ('new—data-sign',self.data_sign)
        #print ('len of datasign',len(self.data_sign) )
        self.data_sign.append(0)
        print ('data_sign:')
        
        
        
        #blurry
        new_seq=[   int(round(
                        
                        1/5*self.data_sign[max(i-2,0)]+
                        1/5*self.data_sign[max(i-1,0)]+
                        1/5*self.data_sign[i]+
                        1/5*self.data_sign[min(i+1,len(self.data_sign)-1)]
                        +1/5*self.data_sign[min(i+2,len(self.data_sign)-1)]
                        
                    ))
                    for i in range(len(self.data_sign))
                ]
        self.data_sign=new_seq
        
        
        draw_pic.draw_pic(self.data_sign,False,a)
        
        pass
    
    def slide_bm_search(self):
        #try bm search with slide wimdow
        #infact only thesmallest time need to do bm search
        self.start_index=[[] for i in self.data_sign]
        #start index [index1,index2,index3]
        #   each index:[[end1,time],[end2,time]]
        #   end will be record when time>1
        #   could get the len by end and start
        #   end ought be sorted
        w=self.min_len
        #first time
        for i in range(len(self.data_sign)):
            start=i
            end=i+w
            print('end',end)
            if end>=len(self.data_sign):
                #goal sub exceed
                break
            sub_seq=self.data_sign[start:end]
            if self.sub_dict.get(hash(tuple(sub_seq)))==None:
                #not search this seq yet
                pattern_array=bm_test.BoyerMooreHorspool(sub_seq,self.data_sign)
                
                if(len(pattern_array))>1:
                    print ('effective sub seq at:',i,'time',len(pattern_array))
                for pos in pattern_array:    
                    self.start_index[pos].append([pos+w,len(pattern_array)])
                #[time(or key value) position]
                #self.sub_seq_information.append([self._value_sub_seq_in_rare(pattern_array,sub_seq),pattern_array,sub_len])
                print('subseq',sub_seq)
                print ('prev_pa',pattern_array)
                self.sub_dict[hash(tuple(sub_seq))]=pattern_array
                #sub_dict record startpos of sub sequence
        print ('ttlen',len(self.data_sign))
        input()
        while w<self.max_len:
            for i in range(len(self.data_sign)):
                start=i
                end=i+w
                print('end',end)
                if end+1>=len(self.data_sign):
                    #goal sub exceed
                    break
                prev_seq=self.data_sign[start:end]
                
                now_seq=[x for x in prev_seq]
                now_seq.append(self.data_sign[end+1])
                print ('prev_seq',prev_seq,len(prev_seq))
                print ('now_seq',now_seq,len(now_seq))
                prev_seq_hash_key=hash(tuple(prev_seq))
                prev_pa=self.sub_dict[prev_seq_hash_key]
                print ('prev_pa',prev_pa)
                now_pa=[start]
                for pos in prev_pa:
                    if pos!=start:
                        #compare w+1 and add to now pattern array
                        temp_end=pos+w+1
                        if temp_end>=len(self.data_sign):
                            pass
                        elif self.data_sign[end+1]==self.data_sign[temp_end]:
                            now_pa.append(pos)
                
                if(len(now_pa))>1:
                    print ('effective sub seq at:',i,'time',len(now_pa))
                for pos in now_pa:    
                    self.start_index[pos].append([pos+w+1,len(now_pa)])            
                self.sub_dict[hash(tuple(now_seq))]=now_pa
                
                
            w=w+1
        
        self._value_sub_seq_in_rare_slide()
        
        
        pass
    
    def bm_search(self):
        #origin version
        
        
        for sub_len in range(self.min_len,self.max_len+1):
            print ('now sublen:',sub_len)
            for i in range(len(self.data_sign)):
            #i is p
                #len of subseq is [min,max]
                
                sub_end=i+sub_len
                if sub_end>=len(self.data_sign):
                    #goal sub exceed
                    break
                sub_seq=self.data_sign[i:sub_end]
                if self.sub_dict.get(hash(tuple(sub_seq)))!=True:
                    #not search this seq yet
                    pattern_array=bm_test.BoyerMooreHorspool(sub_seq,self.data_sign)
                    
                    if(len(pattern_array))>1:
                        print ('effective sub seq at:',i,'time',len(pattern_array))
                        
                    #[time(or key value) position]
                    self.sub_seq_information.append([self._value_sub_seq_in_rare(pattern_array,sub_seq),pattern_array,sub_len])
                    self.sub_dict[hash(tuple(sub_seq))]=True
        #search finished. then sort by value
        self.sub_seq_information=sorted(self.sub_seq_information,key=lambda x:x[0])
        #normalize the value as value
        
        color_value=[x[0] for x in self.sub_seq_information]
        
        #print ('bfcolorvalue',color_value)
        #color_value=Z_ScoreNormalization(color_value,np.average(color_value),np.std(color_value))
        max_v=max(color_value)
        min_v=min(color_value)
        color_value=[int(250*(v-min_v)/(max_v-min_v)) for v in color_value]
        #print ('afcolorvalue',color_value)
        for i in range(len(self.sub_seq_information)):
            self.sub_seq_information[i][0]=color_value[i]
            
        self._fill_color_value()
        pass
    
    def _value_sub_seq_in_rare(self,pattern_array,sub):
        #value by complexity, length, and appearence time
        complexity=np.std(sub)
        leng=len(sub)
        appearence_t=len(pattern_array)
        if appearence_t<2:
            return 0
        _value=leng*(appearence_t-1)
        return _value
    
    def _value_sub_seq_in_rare_slide(self):
        #value in slide window
        #give [value,[start,end]]
        value_of_array=[]
        #start index [index1,index2,index3]
        #   each index:[[end1,time],[end2,time]]
        for i in range(len(self.start_index)):
            count=0
            self.start_index[i]=sorted(self.start_index[i],key=lambda x:x[0])
            for p in self.start_index[i]:
                if p[1]>1:
                    count=count+p[1]-1
                    value=(p[0]-i)*p[1]/count
                    value_of_array.append([value,[i,p[0]]])
        #test
        color_value_array=[10 for x in self.dataseq]
        self.color_value=[]
        value_of_array=sorted(value_of_array,key=lambda x:x[0],reverse=True)
        
        print (value_of_array)
        for pair in value_of_array:
            if pair[0]>70:
                (start,end)=pair[1]
                for i in range(start,end):
                    color_value_array[i]=pair[0]
        self.color_value=color_value_array            
        pass
    def _fill_color_value(self,match_number=6):
        #strgory change: 1match,1color
        
        self.color_value=[]
        for i in range(max(len(self.sub_seq_information),match_number)):
            color_value_array=[10 for x in self.dataseq]
            value=self.sub_seq_information[i][0]
#            if value < 0.75:
#                continue
            position=self.sub_seq_information[i][1]
            temp_len=self.sub_seq_information[i][2]
            for p in position:
                for j in range(temp_len):
                    color_value_array[p+j]=max(value,color_value_array[p+j])
            #self.color_value.append(color_value_array)
            self.color_value=color_value_array
            
        pass
    pass
def Z_ScoreNormalization(x,mu,sigma):  
    x = (x - mu) / sigma;  
    return x;  

if __name__=='__main__':
    
    b=data_builder.data_builder(20,30,1200,0.025,1)
    a=[x for x in range(1200)]
    draw_pic.draw_pic( b.randomlize_xlist,False,a)
    
    b.add_rare(100,80)
    b.add_rare(100,80)
    b.insert_rare_in_rlist()
    c=bm_analyze(60,100, b.randomlize_xlist)
    #c.bm_search()
    c.slide_bm_search()
    a=[x for x in range(len(b.randomlize_xlist))]
    draw_pic.draw_pic( b.randomlize_xlist,False,a)
    #print ('color value',c.color_value)
    
    #for i in range(6):
    draw_pic.draw_pic(c.dataseq,c.color_value,a)
    pass