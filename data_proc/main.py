import parse as p
import gensim as g

l_interested = p.get_entity_list(p.plib.interested_libs)

#l_code = list(map(get_code, l_interested))

l_doc = list(map(p.get_doc, l_interested))
#l_doc = list(map(pdoc.extract, l_doc))

documents = l_doc
texts = p.simple_process(documents=documents, stoplist=p.read_stoplist(p.FNAME_STOPLIST))
texts = p.remove_infrequent(texts, n_times=1)

id2word = g.corpora.Dictionary(texts)
#id2word.save('/tmp/deerwester.dict') # store the id2word, for future reference
print(*list(id2word)[:10])

corpus = [id2word.doc2bow(text) for text in texts]
#g.corpora.corpusCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
print(*list(corpus)[:10])

# load id->word mapping (the id2word), one of the results of step 2 above
#id2word = g.g.corpora.id2word.load_from_text('wiki_en_wordids.txt')
# load corpus iterator
#corpus = g.corpora.MmCorpus('/tmp/deerwester.mm')
#corpus = g.g.corpora.MmCorpus(bz2.BZ2File('wiki_en_tfidf.mm.bz2')) # use this if you compressed the TFIDF output (recommended)

n_topics = 20

## extract 100 LDA topics, using 1 pass and updating once every 1 chunk (10,000 documents)
#lda = g.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=n_topics, 
#                                 update_every=1, chunksize=10000, passes=5)
## print the most contributing words for n_topic topics
#print(*lda.print_topics(n_topics), sep='\n')

# extract 400 LSI topics; use the default one-pass algorithm
lsi = g.models.lsimodel.LsiModel(corpus=corpus, id2word=id2word, num_topics=n_topics)
# print the most contributing words (both positively and negatively) for each of the first n_topic topics
print(*lsi.print_topics(n_topics), sep='\n')

lll = lsi
index = g.similarities.SparseMatrixSimilarity(lll[corpus], num_features=22)
sims = index[lll[id2word.doc2bow(texts[1130])]]
print(list(sorted(enumerate(sims), key=lambda t : t[1], reverse=True))[:10])