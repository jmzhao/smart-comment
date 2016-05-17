# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 20:48:19 2016

@author: jmzhao
"""

import re

ptrn_sharp_com = r'#([^\n]*)(?:$)'

def get_doc(src) :
    """get comments from Python source code
    
    Parameter
    --------------
    src@str - the source code
    """
    pat = re.compile(r'((?:def|class)\s+[^\n]*\s*)"""(.*?)"""',re.MULTILINE|re.DOTALL)
    return [gs for gs in pat.findall(src)]

DISABLE = -1
SIMPLE = 0
ADVANCED = 1
CONCAT = 2

def extract(doc_str, stage=ADVANCED) :
    """
    Get the first "paragraph" in a Python documentation string by passing 
    various stages.
        1. delimited by two newlines.
        2. two lines above any section delimiter (e.g "----" or "====").
        3. concat words broken at end of line (e.e. ending with "-").
    """
    if stage <= DISABLE :
        return doc_str
        
    first_part = doc_str.split('\n\n')[0]
    if stage <= SIMPLE : 
        return first_part
    
    def terminating_line(line) :
        return '---' in line or '===' in line
    def get_desc(para) :
        if len(para) == 0 :
            return
        np = para+['']
        for line, nline in zip(np, np[1:]) :
            if terminating_line(nline) :
                break
            yield line
    desc = list(get_desc([line.strip() for line in first_part.split('\n')]))
    if stage <= ADVANCED :
        return '\n'.join(desc)
        
    for i, line in enumerate(desc[1:]) :
        if desc[i-1][-1] == '-' :
            desc[i-1] = desc[i-1][:-1] + line.split()[0]
            desc[i] = line.split()[1:]
    return '\n'.join(desc)

def main(*argv) :
    filename = argv[1]
    src = open(filename).read()
    print(*get_doc(src),sep="\n")

if __name__ == '__main__' :
    import sys
    main(*sys.argv)