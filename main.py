# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 08:18:32 2018

@author: 赵怀菩
"""

if __name__ == '__main__':
    sitelist=[]
    for file in diskwalk("D:/zhp_workspace/35site").paths():
        print(file)
        filename=file
        #sitelist.append(timeseq(filename))
                