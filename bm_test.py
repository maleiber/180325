# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:00:17 2018

@author: 赵怀菩
"""

def BoyerMooreHorspool(pattern, text):
    m = len(pattern)
    n = len(text)
    ret_val=[]
    if m > n: return []
    skip = []
    for k in range(256): skip.append(m)
    for k in range(m - 1): skip[pattern[k]] = m - k - 1
    skip = tuple(skip)
    k = m - 1
    while k < n:
        j = m - 1; i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1; i -= 1
        if j == -1: ret_val.append(i + 1)
        
        k += skip[text[k]]
    return ret_val

if __name__ == '__main__':
    text = [1,2,3,4,1,2,3]
    pattern = [1,2,3]
    pattern1 = [2,3,4]
    s = BoyerMooreHorspool(pattern, text)
    print ('Text:',text)
    print ('Pattern1:',pattern)
    print ('Pattern2:',pattern1)
    if len(s) > 0:
        print ('Pattern \"' ,pattern , '\" found at position',s)
    s = BoyerMooreHorspool(pattern1, text)
   
    if len(s) > 0:
        print ('Pattern \"' ,pattern1 , '\" found at position',s)