#!/usr/bin/python
#-*-coding:utf8-*-
import gzip
import sys

dia={u'č':'c',u'š':'s',u'ž':'z',u'ć':'c'}
def remove_diacritics(token):
  result=''
  for char in token:
    result+=dia.get(char,char)
  return result

log=open('log','w')
hr={}
sr={}
for line in gzip.open('../../lexicons/apertium/apertium-hbs.hbs_HR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if token.lower()!=token:
    continue
  if token not in hr:
    hr[token]=set()
  hr[token].add(tag)
log.write(repr(hr.items()[:10])+'\n')
for line in gzip.open('../../lexicons/apertium/apertium-hbs.hbs_SR_purist.mte.gz'):
  token,lemma,tag=line.decode('utf8').split('\t')[:3]
  if token.lower()!=token:
    continue
  if token not in sr:
    sr[token]=set()
  sr[token].add(tag)
log.write(repr(sr.items()[:10])+'\n')
for index,token in enumerate(hr):
  if index%100==0:
    log.write(str(index+1)+' od '+str(len(hr))+'\n')
  ijee=token.replace('ije','e')
  jee=token.replace('je','e')
  for mod_token in (ijee,jee):
    if token==mod_token:
      continue
    if mod_token in sr:
      log.write(repr('candidate '+token+' '+mod_token)+'\n')
      if len(hr[token].intersection(sr[mod_token]))>0:
        if mod_token not in hr:
          log.write('not in hr\n')
          sys.stdout.write(token.encode('utf8')+'\tje\n')
          sys.stdout.write(mod_token.encode('utf8')+'\te\n')
          dia_token=remove_diacritics(token)
          if dia_token!=token:
            dia_mod_token=remove_diacritics(mod_token)
            if dia_token not in hr and dia_mod_token not in hr:
              log.write('dia not in lexicons\n')
              sys.stdout.write(dia_token.encode('utf8')+'\tje\n')
              sys.stdout.write(dia_mod_token.encode('utf8')+'\te\n')
          break
