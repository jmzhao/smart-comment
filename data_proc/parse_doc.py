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

def extract(doc) :
    first_part = doc.split('\n\n')[0] # the first "paragraph" delimited by two newlines
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
    desc = list(get_desc([line.strip() for line in first_part.split('\n') if len(line.strip())>0]))
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