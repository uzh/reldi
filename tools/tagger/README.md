## Dependencies

Python modules:

* sklearn(>=0.15)
* marisa_trie
* pycrfsuite

## Training data format

The training data should be in the CoNLL format with the token in the second column and the tag in the fifth column.

## Preparing the lexicon trie

`$ gunzip -c ../../lexicons/apertium/apertium-hbs.hbs_HR_purist.mte.gz | cut -f 1,2,3 | ./prepare_marisa.py hr.marisa`

`$ gunzip -c ../../lexicons/apertium/apertium-hbs.hbs_SR_purist.mte.gz | cut -f 1,2,3 | ./prepare_marisa.py sr.marisa`

## Training the tagger

The only argument given to the script is the language code. In case of Croatian (language code `hr`) the corpus training data is expected to be in the file `hr.conll`, while the lexicon trie is expected to be in the file `hr.marisa`.

`$ ./train_tagger.py hr`

`$ ./train_tagger.py sr`

`$ ./train_tagger.py sl`

## Preparing the lexicon for training the lemmatiser

`$ ./lemma_freq.py hr.lemma_freq < training_data/hr.conll`

`$ ./lemma_freq.py sl.lemma_freq < training_data/sl.conll`

`$ ./lemma_freq.py sr.lemma_freq < training_data/sr.conll`

`$ gunzip -c ~/projects/reldi/reldi/lexicons/apertium/apertium-hbs.hbs_HR_purist.mte.gz | awk '{print $1 "\t" $2 "\t" $3}' | ./prepare_lexicon.py hr.lemma_freq hr.lexicon`

`$ gunzip -c ~/projects/reldi/reldi/lexicons/apertium/apertium-hbs.hbs_SR_purist.mte.gz | awk '{print $1 "\t" $2 "\t" $3}' | ./prepare_lexicon.py sr.lemma_freq sr.lexicon`

## Training the lemmatiser

`$ ./train_lemmatiser.py hr.lexicon`

`$ ./train_lemmatiser.py sr.lexicon`

`$ ./train_lemmatiser.py sl.lexicon`

