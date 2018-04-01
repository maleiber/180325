# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 15:28:19 2018

@author: 赵怀菩
"""
from FT_tree_Node import *

class FP_tree(object):
    #optimized for timing sequence
    def __init__(self,support=2,believe=0.5,window_width=20):
        self.support=support
        #support is min time a signnal appear.
        #    if less than it, the node will be prune after builing a tree
        self.believe=believe
        self.window=window_width
        #believe is min value It think 2 rule have associate
        self.time_seq_data=[]
        pass
    def add_sequence(self,raw_seq):
        #raw_seq must like:
        #    [ [time1,(name1,signal1)],[time2,(name2,signal2)],....]
        #signal must be unique!!
        #need to build a FPTree for a time line
        # one time, one sequence
#        seq_dict={}
#        tree_name=raw_seq[0][1][0]

#        
        self.time_seq_data.append(raw_seq)
        pass
    def init_sub_tree(self):
        self.sub_tree=[]
        self.key2pos_dict={}
        #    key  ,  all position
        self.count_dict={}
        #    key  ,  count
        self.pos2key_dict={}
        #    name , key
        #first child
        for raw_x_seq in self.time_seq_data:
            name=raw_x_seq[0][1][0]
            now_parent=FT_tree_Node(name,'root',0)
            seq_dict={}
            node_inf=[]
            
            #count time
            for pair in raw_x_seq:
                all_position=pair[1][1:]
                self.key2pos_dict[pair[1]]=all_position
                for pos in all_position:
                    if self.pos2key_dict.get(pos)==None:
                        now_key=[]
                    else:
                        now_key=self.pos2key_dict.get(pos)
                    now_key.append([name,pair[1]])
                    #    name , key
                    self.pos2key_dict[pos]=now_key
                    
                if pair[1] in self.count_dict:
                    seq_dict[pair[1]]=seq_dict[pair[1]]+1
                else:
                    seq_dict[pair[1]]=1
                    #count key
                    node_inf=[(seq_dict[key],key) for key in seq_dict if seq_dict[key]>=self.support]
                    #node_inf=sorted(node_inf,key=lambda x:x[0],reverse=True)
                    self.count_dict.update(seq_dict)
            for node_val in node_inf:
                now_node=FT_tree_Node(name,node_val[1],node_val[0],now_parent)
                all_position=node_val[1][1:]
                now_node.set_node_time(all_position)
                now_parent.child[node_val[1]]=now_node
                    
            self.sub_tree.append(now_parent)
        
        #second child
        for now_parent_node in self.sub_tree:        
            for child_key in now_parent_node.child:
                now_node=now_parent_node.child[child_key]
                now_origin_time=now_node.this_node_time
                #(1,3,5,7)
                # time is position array key appear
                accept_pos={}
                #form accept time
                for start in now_origin_time:
                    for i in range(1,self.window):
                        accept_pos[start+i]=1
                accept_pos=[pos for pos in accept_pos]
                #(2,3,4,5,6,7)
                #searching alivable key by accept pos
                key_set={}
                for pos in accept_pos:
                    if self.pos2key_dict.get(pos)==None:
                        continue
                    else:
                        temp_set=self.pos2key_dict[pos]
                        for pair in temp_set:
                            key_set[pair[1]]=pair[0]
                            #key = belonging tree
                #chose the key-char not in this tree and reach the support requirement
                accept_key=[key for key in key_set if key_set[key]!=now_node.name
                                and self.count_dict[key]>=self.support
                            ]
                #now can use acckey to make new node
                for alivable_key in accept_key:
                    #c1,b1
                    #take origin time of c1
                    y_position=alivable_key[1:]
                    #take intersection y and accept pos as new node's time
                    intersection=[x for x in y_position if x in accept_pos]
                    
                    if len(intersection)<self.support:
                        #invalid intersection
                        pass
                    
                    elif now_node.child.get(alivable_key)==None:
                        # new node
                        new_name=alivable_key[0]
                        new_node=FT_tree_Node(new_name,alivable_key,len(intersection),now_node)
                        #take node time information
                        new_node.set_node_time(intersection)
                        new_node.set_parent_time(now_origin_time)
                        #add child
                        now_node.child[alivable_key]=new_node
                        pass
                    else:
                        #error
                        #because accept_key is from key in dict. cant be multiple
                        pass
                
        pass
        
    def merge_sub_tree(self):
        #firstly, build tree for each time sequence
        
        
        
        #merge all the sub tree to one
        #end of fromer and start of latter should be same
        
        #prune branch by  appearence, 
        
        pass
    def get_associate_rule(self):
        pass
    pass

if __name__=='__main__':
    
    pass