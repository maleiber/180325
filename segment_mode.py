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
        self.data_sign=[x for x in self.dataseq]
#        prev=self.dataseq[0]
#
#        #self.data_sign.append(prev)
#        for i in range(len(self.dataseq)-1):
#            now=self.dataseq[i]
#            self.data_sign.append([[prev,now],now-prev])
#            prev=now
#        #finished dx
        a=[i for i in range(len(self.data_sign))]
        draw_pic.draw_pic(self.data_sign,False,a)
        pass
    def _bottom_up_merge(self):
        self.__build_origin_segment()
        # self.data_sign is the origin segment
        # now segment
        threshold=6
        zipshold=0.2
        now_segment=[]
        #element in now segment:
        #    [[point,...],diff]
        #when try to merge now and next:
        #    make point became [nowpoint_start,...,nowpoint_end,nextpointstart,...,nextpointend]
        #    new segment=(next_end - now_start,data_sign[next_end]-data_sign[now_start])
        #    in per dx, step of newsegment is (y/x)  
        #if size of point <=2, diff=0
        #    diff=sum[ abs((p-nowstart)*step-(data[p]-data[nowstart])) for p in point[1:-1] ]
        #                                                                   *expect start and end
        #make now seg init
        for i in range(len(self.data_sign)):
            now_segment.append([[i],0])
        #start iter
        
        #one treverse
        while True:
            alternate_seg=[]
            i=0
            direct_merge_count=0
            while i<len(now_segment)-1:
                now_p,nowdiff=now_segment[i]
                next_p,nextdiff=now_segment[i+1]
                diff=0
                new_p=now_p+next_p
                #caculate diff
                if len(new_p)<=2:
                    diff=0
                elif len(new_p)>self.max_len:
                    # long than max window's width
                    #cannot use
                    diff=threshold
                else:
                    #cacul segment by now_p and next_p
                    x,y=self.__caculate_seg(now_p,next_p)
                    step=y/x
                    nowstart=new_p[0]
                    diff=sum([abs(
                                (p-nowstart)*step -(self.data_sign[p]-self.data_sign[nowstart])
                                )
                                for p in new_p[1:-1]
                            ])
                    
                #judge if merge by diff
                if diff==0:
                    #when diff =0 direct change now segment
                    now_segment.pop(i)
                    now_segment[i]=[new_p,diff]
                    direct_merge_count=direct_merge_count+1
    
                elif diff<threshold:
                    #added to alternate_seg
                    alternate_seg.append([i,new_p,diff])
                #now=next
                i=i+1
            #sorted and chose
            zip_rate=len(now_segment)/len(self.data_sign)
            #print ('zip_rate',zip_rate,'alter:',alternate_seg)
            if len(alternate_seg)>0 and zip_rate>zipshold:
                alternate_seg=sorted(alternate_seg,key=lambda x:x[2])
                #chose one smallest diff
                i,new_p,diff=alternate_seg[0]
                
                #merge
                now_segment.pop(i)
                now_segment[i]=[new_p,diff]
            elif direct_merge_count==0:
                #no more alter_seg  or zip rate pass,break
                break
        #cacul the difference now&next in each of the now segment
        # if difference: <threshold , directly merge it in now segment
        # if not ,merge 1 the lowest in each traverse until zip rate pass
        #  however, the origin length of now segment could not more than w
        #all segment merge finish,then update data_sign
        new_sign=[self.data_sign[0]]
        #the first value always not changed
        for now_p,diff in now_segment:
            
            new_sign.append(self.data_sign[now_p[-1]])
            pass
        #take a picture
        a=[x for x in range(len(new_sign))]
        draw_pic.draw_pic( new_sign,False,a)
        #self.data_sign=new_sign
        
        pass
    def __caculate_seg(self,now_p,next_p):
        new_p=now_p+next_p
        x=new_p[-1]-new_p[0]
        y=self.data_sign[new_p[-1]]-self.data_sign[new_p[0]]
        return (x,y)
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
    #draw_pic.draw_pic( b.randomlize_xlist,False,a)
    
    b.add_rare(100,80)
    b.add_rare(100,80)
    b.insert_rare_in_rlist()
    c=segment_mode(70,100, b.randomlize_xlist)
    pass