#!/usr/bin/python
#-*-coding:utf8-*-

import sys
import os
import kenlm
import cPickle as pickle
from random import randint

tm_lambda=0.2
lm_lambda=0.8

import os
reldir=os.path.dirname(os.path.abspath(__file__))
#os.path.dirname(sys.argv[0])+'/'

def get_uppers(token_list):
  uppers=[]
  for token in token_list:
    uppers.append([])
    for index,char in enumerate(token):
      if char.isupper():
        uppers[-1].append(index)
  return uppers

def apply_uppers(uppers,token_list):
  for token_index,indices in enumerate(uppers):
    token=token_list[token_index]
    for index in indices:
      if index<len(token):
        token=token[:index]+token[index].upper()+token[index+1:]
    token_list[token_index]=token
  return token_list

def redi(token_list,lexicon,lm):
  uppers=get_uppers(token_list)
  token_list=[e.lower() for e in token_list]
  indices=[]
  for index,token in enumerate(token_list):
    if token in lexicon:
      if len(lexicon[token])==1:
        token_list[index]=lexicon[token].keys()[0]
      else:
        if lm==None:
          token_list[index]=sorted(lexicon[token].items(),key=lambda x:-x[1])[0][0]
        else:
          indices.append(index)
  for index in indices:
    hypotheses={}
    for hypothesis in lexicon[token_list[index]]:
      sent=' '.join(token_list[:index]+[hypothesis]+token_list[index+1:])
      hypotheses[hypothesis]=lm_lambda*lm.score(sent)+tm_lambda*lexicon[token_list[index]][hypothesis]
    token_list[index]=sorted(hypotheses,key=lambda x:-hypotheses[x])[0]
  return apply_uppers(uppers,token_list)

def read_and_write(istream,index,ostream,lm):
  entry_list=[]
  for line in istream:
    if line.strip()=='':
      token_list=redi([e[index] for e in entry_list],lexicon,lm)
      ostream.write(''.join(['\t'.join(entry)+'\t'+token+'\n' for entry,token in zip(entry_list,token_list)]).encode('utf8')+'\n')
      entry_list=[]
    else:
      entry_list.append(line[:-1].decode('utf8').split('\t'))

if __name__=='__main__':
  import argparse
  parser=argparse.ArgumentParser(description='Diacritic restoration tool for Slovene, Croatian and Serbian')
  parser.add_argument('lang',help='language of the text',choices=['sl','hr','sr'])
  parser.add_argument('-l','--language-model',help='use the language model',action='store_true')
  parser.add_argument('-i','--index',help='index of the column to be processed',type=int,default=0)
  args=parser.parse_args()
  lexicon=pickle.load(open(os.path.join(reldir,'wikitweetweb.'+args.lang+'.tm')))
  if args.language_model:
    cnf=kenlm.Config()
    cnf.load_method=0
    lm=kenlm.LanguageModel(os.path.join(reldir,'wikitweetweb.'+args.lang+'.bin'),cnf)
  else:
    lm=None
  read_and_write(sys.stdin,args.index-1,sys.stdout,lm)
