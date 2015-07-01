#!/bin/bash
#grep -v ' lang="hr"' apertium-hbs.hbs.metadix > apertium-hbs.hbs_HR_purist.metadix
xsltproc --stringparam alt hbs_SR_purist --stringparam var ek alt.xsl apertium-hbs.hbs.metadix > .deps/apertium-hbs.hbs_SR_purist.dix
#rm apertium-hbs.hbs_HR_purist.metadix
lt-expand .deps/apertium-hbs.hbs_SR_purist.dix | python export-lexicon.ap-me.py > apertium-hbs.hbs_SR_purist.mte
awk '{if (substr($3,1,1)!="P") print $0}' apertium-hbs.hbs_SR.mte > temp
cat MTE_pronouns.txt >> temp
mv temp apertium-hbs.hbs_SR_purist.mte
