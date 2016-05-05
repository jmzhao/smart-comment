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
        
FNAME_STOPLIST = '../data/SmartStoplist.txt'

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


texts = simple_process(documents=documents, stoplist=read_stoplist(FNAME_STOPLIST))
texts = remove_infrequent(texts, n_times=1)

dictionary = g.corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict') # store the dictionary, for future reference
#print(dictionary)

corpus = [dictionary.doc2bow(text) for text in texts]
g.corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
#print(corpus)

# load id->word mapping (the dictionary), one of the results of step 2 above
id2word = dictionary #g.g.corpora.Dictionary.load_from_text('wiki_en_wordids.txt')
# load corpus iterator
mm = g.corpora.MmCorpus('/tmp/deerwester.mm')
# mm = g.g.corpora.MmCorpus(bz2.BZ2File('wiki_en_tfidf.mm.bz2')) # use this if you compressed the TFIDF output (recommended)

print(mm)

# extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
lda = g.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=20, 
                                 update_every=1, chunksize=10000, passes=5)
# print the most contributing words for 20 randomly selected topics
print(*lda.print_topics(20), sep='\n')

index = g.similarities.SparseMatrixSimilarity(lda[corpus], num_features=22)
sims = index[lda[dictionary.doc2bow(texts[51])]]
print(list(sorted(enumerate(sims), key=lambda t : t[1], reverse=True))[:10])

## extract 400 LSI topics; use the default one-pass algorithm
#lsi = g.models.lsimodel.LsiModel(corpus=mm, id2word=id2word, num_topics=400)
#
## print the most contributing words (both positively and negatively) for each of the first ten topics
#lsi.print_topics(10)

if __name__ == '__main__' :
    pass