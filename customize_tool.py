# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 21:12:13 2018

@author: 赵怀菩
"""
import numpy
def Z_ScoreNormalization(x):
    mu=numpy.average(x)
    sigma=numpy.std(x)
    x = (x - mu) / sigma;  
    return x;  
def cos(vector1,vector2):  
    dot_product = 0.0;  
    normA = 0.0;  
    normB = 0.0;  
    for a,b in zip(vector1,vector2):  
        dot_product += a*b  
        normA += a**2  
        normB += b**2  
    if normA == 0.0 or normB==0.0:  
        #return None
        return 0
    else:  
        return dot_product / ((normA*normB)**0.5)  