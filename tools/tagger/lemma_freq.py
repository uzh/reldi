#!/usr/bin/python
import sys
import cPickle as pickle

lemma_freq={}
for line in sys.stdin:
  try:
    lemma=line.decode('utf8').split('\t')[2].lower()
  except:
    continue
  lemma_freq[lemma]=lemma_freq.get(lemma,0)+1
print lemma_freq.items()[:10]
pickle.dump(lemma_freq,open(sys.argv[1],'w'),1)