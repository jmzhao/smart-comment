# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 12:00:39 2016

@author: jmzhao
"""

import comments
import gensim as g

with open('../../dataset_python3/scikit.txt') as src_file :
    l_comments = comments.get_comments(src_file.read())
    documents = [t[1].split('\n\n')[0] for t in l_comments]

# remove common words and tokenize
stoplist = set(open('../../RAKE-tutorial/SmartStoplist.txt').read().split())
stemmer = g.parsing.PorterStemmer()
texts = [[stemmer.stem(word) for word in g.utils.tokenize(document, to_lower=True) if word not in stoplist]
         for document in documents]

# remove words that appear only once
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
        
texts = [[token for token in text if frequency[token] > 1]
         for text in texts]

from pprint import pprint   # pretty-printer
pprint(texts)

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
lda = g.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=20, update_every=1, chunksize=10000, passes=1)
# print the most contributing words for 20 randomly selected topics
print(*lda.print_topics(10), sep='\n')

index = g.similarities.SparseMatrixSimilarity(lda[corpus], num_features=22)
sims = index[lda[dictionary.doc2bow(texts[51])]]
print(list(enumerate(filter(lambda x : x >0.5, sims))))

## extract 400 LSI topics; use the default one-pass algorithm
#lsi = g.models.lsimodel.LsiModel(corpus=mm, id2word=id2word, num_topics=400)
#
## print the most contributing words (both positively and negatively) for each of the first ten topics
#lsi.print_topics(10)