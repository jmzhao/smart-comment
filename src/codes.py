
# coding: utf-8

# In[3]:

import data
import gensim as g
import inspect
import dis
import itertools


# In[4]:

# gather Python entities from libraries
l_interested = data.get_entity_list(data.libinfo.interested_libs)
l_code = list(map(data.get_code, l_interested))


# In[27]:

print(*(i for i in dis.get_instructions(l_code[1234])), sep='\n')


# In[5]:

l_ins = [[i.opname for i in dis.get_instructions(code)]
        for code in l_code]
all_ins = list(itertools.chain(*l_ins))
print(len(all_ins))
all_ins_unique = set(all_ins)
print(len(all_ins_unique))


# In[13]:

model = g.models.word2vec.Word2Vec(l_ins, size=8, window=10, min_count=1, workers=4, seed=1337, iter=20)


# In[21]:

print(*[x for i, x in model.most_similar(positive=['BINARY_ADD'])], sep='\n')


# In[30]:

print(*["(%s)"%', '.join("%.2f"%x for x in model[i]) for i, _ in model.most_similar(positive=['BINARY_ADD'])], sep='\n')


# In[31]:

"(%s)"%', '.join("%.2f"%x for x in model['BINARY_ADD'])


# In[54]:

all_ins_unique


# In[6]:

import numpy as np
np.amax([len(x) for x in l_ins])


# In[ ]:



