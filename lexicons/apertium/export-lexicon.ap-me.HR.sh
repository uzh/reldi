#!/bin/bash
grep -v ' lang="sr"' apertium-hbs.hbs.metadix > apertium-hbs.hbs_HR_purist.metadix
xsltproc --stringparam alt hbs_HR_purist --stringparam var ijek alt.xsl apertium-hbs.hbs_HR_purist.metadix > .deps/apertium-hbs.hbs_HR_purist.dix
rm apertium-hbs.hbs_HR_purist.metadix
#lt-expand .deps/apertium-hbs.hbs_HR_purist.dix | python export-lexicon.ap-me.py > apertium-hbs.hbs_HR_purist.mte
#awk '{if (substr($3,1,1)!="P") print $0}' apertium-hbs.hbs_HR_purist.mte > temp
#cat MTE_pronouns.txt >> temp
#mv temp apertium-hbs.hbs_HR_purist.mte
