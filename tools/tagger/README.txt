## Dependencies
Python modules:
sklearn(>=0.15)
marisa_trie
pycrfsuite

## Training data format

The training data should be in the CoNLL format with the token in the second
column and the tag in the fifth column.

###PREPARING THE LEXICON TRIE###
gunzip -c ~/projects/reldi/reldi/lexicons/apertium/apertium-hbs.hbs_HR_purist.mte.gz | awk '{print $1 "\t" $2 "\t" $3}' | ./prepare_marisa.py hr.marisa
gunzip -c ~/projects/reldi/reldi/lexicons/apertium/apertium-hbs.hbs_SR_purist.mte.gz | awk '{print $1 "\t" $2 "\t" $3}' | ./prepare_marisa.py sr.marisa
gunzip -c ../2-lexicon/sl/sloleks-en_v1.2.tbl.gz | awk '{print $1 "\t" $2 "\t" $3}' | ./prepare_marisa.py sl.marisa
###PREPARING THE LEXICON FOR TRAINING THE LEMMATISER###
./lemma_freq.py hr.lemma_freq < training_data/hr.conll
./lemma_freq.py sl.lemma_freq < training_data/sl.conll
./lemma_freq.py sr.lemma_freq < training_data/sr.conll
gunzip -c ~/projects/reldi/reldi/lexicons/apertium/apertium-hbs.hbs_HR_purist.mte.gz | awk '{print $1 "\t" $2 "\t" $3}' | ./prepare_lexicon.py hr.lemma_freq hr.lexicon
gunzip -c ~/projects/reldi/reldi/lexicons/apertium/apertium-hbs.hbs_SR_purist.mte.gz | awk '{print $1 "\t" $2 "\t" $3}' | ./prepare_lexicon.py sr.lemma_freq sr.lexicon
gunzip -c ../2-lexicon/sl/sloleks-en_v1.2.tbl.gz | awk '{print $1 "\t" $2 "\t" $3}' | ./prepare_lexicon.py sl.lemma_freq sl.lexicon
###TRAINING THE LEMMATISER###
./train_lemmatiser.py hr.lexicon
./train_lemmatiser.py sr.lexicon
./train_lemmatiser.py sl.lexicon
###TRAINING THE TAGGER###
./train_tagger.py hr
./train_tagger.py sr
./train_tagger.py sl
