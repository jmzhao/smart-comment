
# coding: utf-8

# In[1]:

import data
import topicmodeling as tp
import gensim as g


# In[33]:

l_interested = list(set(data.get_entity_list(data.libinfo.interested_libs)))
print(len(l_interested))
#l_code = list(map(data.get_code, l_interested))
l_doc = list(map(data.get_doc, l_interested))
l_doc = list(map(lambda doc : data.pdoc.extract(doc, stage=data.pdoc.ADVANCED), l_doc))


# In[34]:

documents = l_doc
texts = tp.simple_process(documents=documents, stoplist=tp.read_stoplist("../SmartStoplist.txt"))
texts = tp.remove_infrequent(texts, n_times=1)


# In[35]:

id2word = g.corpora.Dictionary(texts)
#id2word.save('/tmp/deerwester.dict') # store the id2word, for future reference
print(*list(id2word)[:10])


# In[36]:

corpus = [id2word.doc2bow(text) for text in texts]
#g.corpora.corpusCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
print(*list(corpus)[:10])
tfidf = g.models.tfidfmodel.TfidfModel(corpus)
corpus = [tfidf[bag] for bag in corpus]
print(*list(corpus)[:10])


# In[ ]:

# load id->word mapping (the id2word), one of the results of step 2 above
#id2word = g.g.corpora.id2word.load_from_text('wiki_en_wordids.txt')
# load corpus iterator
#corpus = g.corpora.MmCorpus('/tmp/deerwester.mm')
#corpus = g.g.corpora.MmCorpus(bz2.BZ2File('wiki_en_tfidf.mm.bz2')) # use this if you compressed the TFIDF output (recommended)


# In[81]:

n_topics = 40
## extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
lda = g.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=n_topics, 
                                 update_every=1, chunksize=10000, passes=5)
## print the most contributing words for n_topic topics
l = list(lda.print_topics(n_topics))
for i, s in l :
    print(i, *s.split(' + '))


# In[ ]:

n_topics = 20
## extract 400 LSI topics; use the default one-pass algorithm
#lsi = g.models.lsimodel.LsiModel(corpus=corpus, id2word=id2word, num_topics=n_topics)
## print the most contributing words (both positively and negatively) for each of the first n_topic topics
#print(*lsi.print_topics(n_topics), sep='\n')


# In[86]:

lll = lda
#index = g.similarities.SparseMatrixSimilarity(lll[corpus], num_features=22)
index = g.similarities.Similarity(None, lll[corpus], num_features=n_topics)


# In[89]:

i_doc = 1589
sims = index[lll[id2word.doc2bow(texts[i_doc])]]
print(i_doc, '', data.pdoc.extract(l_interested[i_doc].__doc__), sep=' | ')
for i, score in list(sorted(enumerate(sims), key=lambda t : t[1], reverse=True))[:10] :
    print(i, "%.3f"%score, data.pdoc.extract(l_interested[i].__doc__), sep=' | ')



