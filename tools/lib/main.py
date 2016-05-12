from lexicon import Lexicon
from tagger import Tagger
from lemmatiser import Lemmatiser
from restorer import DiacriticRestorer
from getpass import getpass

if __name__ == "__main__":
    lex = Lexicon('hr')
    passwd=getpass('Input password: ')
    lex.authorize("user", passwd)
    print "======== Lexicon output ========"
    print lex.queryEntiries(surface="pet")
    print

    print "======== Diacritic restorer output ========"
    restorer = DiacriticRestorer('sr')
    restorer.authorize("user", passwd)
    print restorer.restore('Ucitani su modeli prije zetve! cao djaci! sto mu gromova...')
    print

    print "======== Tagger output ========"
    tagger = Tagger('hr')
    tagger.authorize("user", passwd)
    e=tagger.tag('Modeli su super? Nisu!')
    print
    print tagger.tagLemmatise('Modeli su super')
    print

    print "======== Lemmatiser output ========"
    lemmatiser = Lemmatiser('hr')
    lemmatiser.authorize("user", passwd)
    print lemmatiser.lemmatise('Modeli su super')
    print lemmatiser.lemmatise("""
        <?xml version="1.0" encoding="UTF-8"?>
            <D-Spin xmlns="http://www.dspin.de/data" version="0.4">
            <MetaData xmlns="http://www.dspin.de/data/metadata"/>
            <TextCorpus xmlns="http://www.dspin.de/data/textcorpus" lang="hr">
               <text>Modeli su super</text>
            </TextCorpus>
        </D-Spin>""", format='tcf')