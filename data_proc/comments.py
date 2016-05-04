# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 20:48:19 2016

@author: jmzhao
"""

import re

ptrn_sharp_com = r'#([^\n]*)(?:$)'

def get_comments(src) :
    """get comments from Python source code
    
    Parameter
    --------------
    src@str - the source code
    
    Remark
    -----------
    for demo
    """
    pat = re.compile(r'((?:def|class)\s+[^\n]*\s*)"""(.*?)"""',re.MULTILINE|re.DOTALL)
    return [gs for gs in pat.findall(src)]

def main(*argv) :
    filename = argv[1]
    src = open(filename).read()
    print(*get_comments(src),sep="\n")

if __name__ == '__main__' :
    import sys
    main(*sys.argv)