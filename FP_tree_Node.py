# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 19:29:30 2018

@author: 赵怀菩
"""

class FT_tree_Node(object):
    def __init__(self,name,key,time,parent=None):
        self.name=name
        #name is belonging name of its tree
        self.key=key
        self.parent=parent
        self.child={}
        pass
    def set_parent_time(self,parent):
        self.parent_node_time=parent
        pass
    def set_node_time(self,now):
        self.this_node_time=now
        pass
    def show(self,index=1):
        print(' '*index,self.name,' ',self.count)
        for child in self.child.values():
            child.show(index+1)
    pass