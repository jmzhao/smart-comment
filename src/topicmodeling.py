# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 12:00:39 2016

@author: jmzhao
"""

import re
import gensim as g

PAT_ALPHABETIC = re.compile('(((?![\d])\w)+)', re.UNICODE)
PAT_WORD = re.compile("(((?![\d])[\w'])+)", re.UNICODE)

def tokenize(text, to_lower=False, deacc=False, errors="strict"):
    """
    Iteratively yield tokens as unicode strings, removing accent marks
    and optionally lowercasing the unidoce string by assigning True
    to to_lower.
    
    Note
    ==========
    This is adapted from gensim.utils.tokenize
    """
    lowercase = to_lower
    text = g.utils.to_unicode(text, errors=errors)
    if lowercase:
        text = text.lower()
    if deacc:
        text = g.utils.deaccent(text)
    for match in PAT_WORD.finditer(text):
        yield match.group()

def read_stoplist(fname) :
    """
    Read stop words from a text file, and ignore comments after '#'.
    
    The file contains a stop word per line. 
    """
    stoplist = open(fname).read().split()
    stoplist = filter(lambda line : len(line.strip())>0 and line.strip()[0] != '#', stoplist)
    stoplist = map(lambda line : line.split('#')[0].strip(), stoplist)
    return set(stoplist)
    
def simple_process(documents, stoplist, 
                   tokenizer=lambda doc : g.utils.tokenize(doc, to_lower=True), 
                   stemmer=g.parsing.PorterStemmer()) : 
    texts = [[stemmer.stem(word) for word in tokenizer(document) if word not in stoplist]
             for document in documents]
    texts = [[word for word in text if word not in stoplist]
             for text in texts]
    return texts
    

def remove_infrequent(texts, n_times) :
    """
    remove words that appear fewer than n_times.
    """
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
            
    texts = [[token for token in text if frequency[token] > n_times]
             for text in texts]
    return texts



if __name__ == '__main__' :
    pass