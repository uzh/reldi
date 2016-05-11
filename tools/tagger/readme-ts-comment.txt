# Tagger and lemmatiser for Croatian, Slovene and Serbian

## Dependencies

Python modules:

* sklearn(>=0.15) (necessary only if you want to perform lemmatisation as well)
* marisa_trie
* pycrfsuite

#TS How to check if the dependencies (sklearn, mrisa_trie, pycrfsuite) are already installed on your system? Say what to do if not

## Running the tagger

If you have all the files in place for tagging (for Croatian `hr.msd.model` and `hr.marisa`), you can run the tagger like this:

```
$ ./tagger.py hr
Moj
alat
radi
dobro
.
#TS mention that input needs to be entered manually from the command line in this case
CTRL+D 
#TS for some reason this does not work sometimes, it worked once, but now you exit the program with this command with no results  

Moj	Ps1msn
alat	Ncmsn
radi	Vmr3s
dobro	Rgp
.	Z
```

You can, of course, send the data to be tagged to stdin. Additionally, there is a tokeniser in this toolkit, so probably the most convenient way of running the tagger is this:

```
$ echo 'Moj alat radi dobro.' | ../tokeniser/tokeniser.py hr | ./tagger.py hr
1.1.1.1-3	Moj	Ps1msn
1.1.2.5-8	alat	Ncmsn
1.1.3.10-13	radi	Vmr3s
1.1.4.15-19	dobro	Rgp
1.1.5.20-20	.	Z
```
#TS OK


Run `./tagger.py -h` for additional options.


If you want to use both the tagger and the lemmatiser, you should train the lemmatiser as described below OR get the files for guessing the lemmas from these locations:
#TS why do we have two possibilites here? it might be a better idea to just stick to one

* http://nlp.ffzg.hr/data/reldi/hr.lexicon.guesser
* http://nlp.ffzg.hr/data/reldi/sr.lexicon.guesser
* http://nlp.ffzg.hr/data/reldi/sl.lexicon.guesser
#TS maybe give the commands or say that they can simply find the files with a browser and download

At the end of the process, for Croatian you should have the following files: `hr.lexicon` and `hr.lexicon.guesser`.

Once you have everything in place, just add the `-l` flag to the tagger:

```
$ echo 'Moj alat radi dobro.' | ../tokeniser/tokeniser.py hr | ./tagger.py hr -l
1.1.1.1-3	Moj	Ps1msn	moj
1.1.2.5-8	alat	Ncmsn	alat
1.1.3.10-13	radi	Vmr3s	raditi
1.1.4.15-19	dobro	Rgp	dobro
1.1.5.20-20	.	Z	.
```
#TS OK

## Training your own models

As currently we do not disseminate the lemma prediction models (too large for GitHub), if you want to have lemma prediction models based on the latest version of the lexicon (later than 2016-03-23), you should train your own model. Models for tagging and lexicon files for lemmatisation of know words are included in this distribution.
#TS not perfectly clear: are these guesser files that I just downloaded? what does it mean to be based on the latest version of the lexicon?
#TS why do we talk about tagging models here? What are lexicon files in this whole story? *known* words

### Tagger training data format

The tagger training data should be in the CoNLL format with the token in the second column and the tag in the fifth column.

### Preparing the lexicon trie used by the tagger

The lexicon trie is used both during training the tagger and during tagging.

The examples below should work out-of-the-box for Croatian and Serbian only as we do not currently distribute the Slovene inflectional lexicon.

```
$ gunzip -c ../../lexicons/apertium/apertium-hbs.hbs_HR_purist.mte.gz | cut -f 1,2,3 | ./prepare_marisa.py hr.marisa

$ gunzip -c ../../lexicons/apertium/apertium-hbs.hbs_SR_purist.mte.gz | cut -f 1,2,3 | ./prepare_marisa.py sr.marisa

$ gunzip -c sloleks-en_v1.2.tbl.gz | cut -f 1,2,3 | ./prepare_marisa.py sl.marisa
```

### Training the tagger

The only argument given to the script is the language code. In case of Croatian (language code `hr`) the corpus training data is expected to be in the file `hr.conll`, while the lexicon trie is expected to be in the file `hr.marisa`.

```
$ ./train_tagger.py hr

$ ./train_tagger.py sr

$ ./train_tagger.py sl
```

### Preparing the lexicon for training the lemmatiser

The first step in producing the lexicon for lemmatisation is to calculate the lemma frequency list from the tagger training data. The data in the same format as for training the tagger should be used.

```
$ ./lemma_freq.py hr.lemma_freq < hr.conll

$ ./lemma_freq.py sr.lemma_freq < sr.conll
```

The second step produces the lexicon in form of a `marisa_trie.BytesTrie`. The lemma frequency information is used in case of `(token,msd)` pair collisions. Only the most frequent lemma is kept in the lexicon.

```
$ gunzip -c ../../lexicons/apertium/apertium-hbs.hbs_HR_purist.mte.gz | cut -f 1,2,3 | ./prepare_lexicon.py hr.lemma_freq hr.lexicon

$ gunzip -c ../../lexicons/apertium/apertium-hbs.hbs_SR_purist.mte.gz | cut -f 1,2,3 | ./prepare_lexicon.py sr.lemma_freq sr.lexicon

$ gunzip -c sloleks-en_v1.2.tbl.gz | cut -f 1,2,3 | ./prepare_lexicon.py sl.lemma_freq sl.lexicon

```

### Training the lemmatiser

The lemmatiser of unknown words is trained on the lexicon prepared in the previous step. The lexicon used for training the lemma guesser has a suffix `.train`. A Multinomial Naive Bayes classifier is learned for each MSD. The classes to be predicted are quatruple transformations in form `(remove_start,prefix,remove_end,suffix)`. The transformation is being applied by removing the first remove_start characters, adding the prefix, removing the last remove_end characters and adding the suffix.

The output of the lemmatiser learning process is a file with the `.lexicon.guesser` suffix.

```
$ ./train_lemmatiser.py hr.lexicon

$ ./train_lemmatiser.py sr.lexicon

$ ./train_lemmatiser.py sl.lexicon
```

