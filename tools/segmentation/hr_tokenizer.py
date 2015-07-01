#!/usr/bin/python
#-*-encoding:utf-8-*-
import re
import codecs
import sys
from xml.sax.saxutils import escape,unescape

def unescapefull(s):
  return unescape(s, {"&apos;": "'", "&quot;": '"'})

def escapefull(s):
  return escape(s,{"'":"&apos;",'"':"&quot;"})

def tokenize(paragraph,xml=True):
  sentence=re.compile(u'(?<=[.!?…])(?<!\d\.)(?<!Dr\.|dr\.|Bl\.|bl\.|Pl\.|pl\.|sc\.|Mr\.|mr\.|Sv\.|sv\.)(?<!inž\.|ing\.|iur\.|oec\.|tzv\.)(?<!Akad\.|akad\.|Mons\.|mons\.|Msgr\.|msgr\.|Prof\.|prof\.)\s+(?=[-»"\' ]*[A-ZČĆŠĐŽ])',re.UNICODE)
  # tokenize in two steps - first split by \s+, second apply <g/> everywhere where needed? punct ,;:
  #token=re.compile(r'\s+',re.UNICODE)
  token=re.compile(r'[a-zšđčćž]\.|bl\.|br\.|dr\.|ek\.|fr\.|kr\.|mn\.|mr\.|po\.|pl\.|pr\.|sc\.|sl\.|st\.|sv\.|tj\.|čit\.|eng\.|god\.|hrv\.|inž\.|ing\.|itd\.|iur\.|kbr\.|kem\.|npr\.|oec\.|tal\.|tzv\.|usp\.|vlč\.|akad\.|bacc\.|emer\.|farm\.|gosp\.|mlrd\.|mons\.|msgr\.|prof\.|spec\.|d\.\s?o\.\s?o\.?|\d+(?:[.,:]\d+)*[.]?|&#?[a-z0-9]+;|https?://[-\w/%]+(?:[.#?=&@;][-\w/%]+)+|[\w.-]+@\w+(?:[.-]\w+)+|[@\w]+(?:[.-][@\w]+)*|\.{2,}|[][.,;"\'?():-_/@`»«…£€$%&-]',re.UNICODE|re.IGNORECASE)
  result=''
  for index,sent in enumerate(sentence.split(paragraph)):
    #print sent.encode('utf8')
    sent='\n'.join(token.findall(sent))
    if len(sent)>0:
      if xml:
        result+='<s>\n'+'\n'.join(token.findall(sent))+'\n</s>\n'
      else:
        result+='\n'.join(token.findall(sent))+'\n\n'
  return result

if __name__=='__main__':

  for line in sys.stdin:
    line=line.decode('utf8')
    if len(sys.argv)>1:
      if not line.startswith('<p'):
        sys.stdout.write(line.encode('utf8'))
        continue
      i=line.find('>')+1
      s=line[:i]+'\n'
      s+=tokenize(unescapefull(line[i:-5]))+'</p>\n'
    else:
      s=tokenize(line,False)
    sys.stdout.write(s.encode('utf8'))
