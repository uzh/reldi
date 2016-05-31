#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import re
from datetime import datetime

sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def case(s):
	if s == u'nom':
		return u'n'
	elif s == u'gen':
		return u'g'		
	elif s == u'dat':
		return u'd'
	elif s == u'acc':
		return u'a'
	elif s == u'loc':
		return u'l'
	elif s == u'voc':
		return u'v'
	elif s == u'ins':
		return u'i'

def number(s):
	if s == u'sg':
		return u's'
	elif s == u'pl':
		return u'p'
	elif s == u'sp':
		return u's'
	else:
		return False

def gender(s):
	if s == u'ma' or s == u'mi' or s == u'm':
		return u'm'
	elif s == u'f':
		return u'f'
	elif s == u'nt':
		return u'n'
	elif s == u'mfn':
		return u'-'
	else:
		return False
				
def person(s):
	if s == u'p1':
		return u'1'
	elif s == u'p2':
		return u'2'
	elif s == u'p3':
		return u'3'
	else:
		return False
		
def is_number(s):
    try:
        float(s)
        return u'd'
    except ValueError:
        return u'l'
        
def check_transitivity(s):
	if s == u'tv':
		return u't'
	elif s == u'iv':
		return u'i'
	else:
		return False        
        
def end():		
	if lf not in lexiconout:
		if tags[0] != u'adj' or (tags[0] != u'n' and len(tags) < 6) or (tags[0] != u'np' and len(tags) < 6):
			lexiconout[lf]={sf:set([taglist])}
			if taglist2 != u'' and taglist3 != u'':
				lexiconout[lf]={sf:set([taglist2])}
				lexiconout[lf]={sf:set([taglist3])}
	elif sf not in lexiconout[lf]:
		if tags[0] != u'adj' or (tags[0] != u'n' and len(tags) < 6) or (tags[0] != u'np' and len(tags) < 6):
			lexiconout[lf][sf]=set([taglist])
			if taglist2 != u'' and taglist3 != u'':
				lexiconout[lf][sf]=set([taglist2])
				lexiconout[lf][sf]=set([taglist3])
	elif taglist not in lexiconout[lf][sf]:
		if tags[0] != u'adj' or (tags[0] != u'n' and len(tags) < 6) or (tags[0] != u'np' and len(tags) < 6):
			lexiconout[lf][sf].add(taglist)
			if taglist2 != u'' and taglist3 != u'':
				lexiconout[lf][sf].add(taglist2)
				lexiconout[lf][sf].add(taglist3)
		
lexiconin={}
lexiconout={}
adjout=set()
trans_hash={}
#bejsikli - {lema: {sf: tags}} i onda if (sf, tags) not in lema dodaj, if in lema continue

c=0
		
for i in sys.stdin:
	c+=1
	fields = i.replace('~','').strip().split(u':') #removing post-generator flag as well
	#if fields[1] == u'>':
	#	continue
	if i.startswith('__REGEXP__'):
	  continue
	sf = fields[0]
	if len(sf.split(u' '))>1:
		#vidjet kaj s multiword expressionima - niš
		continue
	if len(fields) == 2:
		lf = re.split(u'<|>',fields[1])[0]
		tags = re.split(u'<|>',fields[1])[1:]
	elif len(fields) == 3:
		lf = re.split(u'<|>',fields[2])[0]
		tags = re.split(u'<|>',fields[2])[1:]
	while u'' in tags:
		tags.remove(u'')
        if c%100000==0:
                sys.stderr.write(datetime.now().isoformat()+' read '+str(c)+'\n')
	#print sf,lf,tags
#sys.exit()
	if tags[0] == u'adj' or (tags[0] == u'n' and len(tags) > 5) or (tags[0] == u'np' and len(tags) > 5):
		tags=tuple(tags)
		if lf not in lexiconin:
			lexiconin[lf]={sf:set(tags)}
		elif sf not in lexiconin[lf]:
			lexiconin[lf][sf]=set(tags)
		elif tags not in lexiconin[lf][sf]:
			lexiconin[lf][sf].add(tags)
		else:
			continue

	taglist = u''
	taglist2 = u'' #these extra two are for <mfn> gender
	taglist3 = u''
	
	transitivity = u''
	
	# punctuation tags
	if tags[0] in [u'sent', u'cm', u'apos', u'guio', u'lpar', u'rpar']:
		taglist+=u'Z'
		#isprintaj samo Z i idi dalje
		end()
		continue
		
	#particle tags
	if tags[0] == u'part':
		if len(tags)>5:
        #print tags
			if tags[3]=='vbser':#Var3s-y
				taglist+='Var'
				taglist+=person(tags[6])
				taglist+=number(tags[7])
				taglist+='-y'
				lf='biti'
				end()
				continue
			elif tags[2]=='+htjeti':
				taglist+='Var'
				taglist+=person(tags[6])
				taglist+=number(tags[7])
				taglist+='-y'
				lf='htjeti'
				end()
				continue
			elif tags[2]==u'+moći':
				taglist+='Vmm'
				taglist+=person(tags[5])
				taglist+=number(tags[6])
				taglist+='-y'
				lf=u'moći'
				end()
				continue
		taglist+=u'Q'
		if len(tags) > 1:
			if tags[1] == u'neg':
				taglist+=u'z'
			elif tags[1] == u'itg':
				taglist+=u'q'
			else:
				if lf=='da':
					taglist+='r'
				else:
					taglist+='o'
		end()
		continue
	
	#adverb tag
	if tags[-1] == u'adv':
		if len(tags) == 1:
			taglist+=u'Rgp'
		elif tags[1] == u'neg':
			if tags[2] == u'imperf':
				taglist+=u'Rr'		
			elif tags[2] == u'perf':
				taglist+=u'Rs'
		else:
			if tags[1] == u'imperf':
				taglist+=u'Rr'		
			elif tags[1] == u'perf':
				taglist+=u'Rs'
		end()
		continue
        #what about adverbs having additional tags? comp sup etc.
	if tags[0]=='adv':
		if tags[1]=='comp':
			taglist+='Rgc'
		elif tags[1]=='sup':
			taglist+='Rgs'
		else:
			taglist+='Rgp'
		end()
		continue
	
	#common noun tags
	if tags[0] == u'n' and len (tags) < 6:
		if lf[0].lower()!=lf[0]:
		  taglist+=u'Np'
		else:
		  taglist+=u'Nc'
		taglist+=gender(tags[1])
		taglist+=number(tags[2])
		taglist+=case(tags[3])
		if tags[3]==u'acc' and tags[2]=='sg':
			if tags[1] == u'ma':
				taglist+=u'y'
			elif tags[1] == u'mi':
				taglist+=u'n'
	#proper noun tags		
	elif tags[0] == u'np' and len (tags) < 6:
		taglist+=u'Np'
		taglist+=gender(tags[2])
		taglist+=number(tags[3])
		taglist+=case(tags[4])
		if tags[4] == u'acc' and tags[3]=='sg':
			if tags[2] == u'ma':
				taglist+=u'y'
			elif tags[2] == u'mi':
				taglist+=u'n'

	#abbreviation tags
	if tags[0] == u'abbr':
		if len(tags) == 1:
			taglist+=u'Y'
			end()
			continue
		elif len(tags) == 2:
			taglist+=u'Npms'
			taglist+=case(tags[1])
			if tags[1] == u'acc':
				taglist+=u'n'
			end()
			continue
		elif len(tags) == 3:
			taglist+=u'Npm'
			taglist+=number(tags[1])
			taglist+=case(tags[2])
			if tags[2] == u'acc':
				taglist+=u'n'
			end()
			continue
		#possessive		
		elif len(tags) > 3:
			taglist+=u'Asp'
			taglist+=gender(tags[3])
			taglist+=number(tags[4])
			taglist+=case(tags[5])
			if tags[5] == u'acc' and tags[4] == u'sg':
				if tags[3] == u'ma':
					taglist+=u'y'
				elif tags[3] == u'mi':
					taglist+=u'n'							
	
	#verb tags
	if tags[0] == u'vblex' or tags[0] == u'vbhaver':
		if tags[3]==u'pp': #<vblex><perf><tv><pp><ma><sg><nom><ind>
			taglist+=u'App'
			if True:
				taglist+=gender(tags[4])
				if tags[5] == u'du':
					continue
				else:
					taglist+=number(tags[5])
				taglist+=case(tags[6])
				if tags[-1]=='def':
				  taglist+='y'
				else:
				  taglist+='n'				
				if tags[6] == u'acc' and tags[5] == u'sg':
					if tags[4] == u'ma':
						taglist+=u'y'
					elif tags[4] == u'mi':
						taglist+=u'n'
				try:
					transitivity+=check_transitivity(tags[2])
				except:
					pass
		else:
			taglist+=u'Vm'
			if lf == u'nemati':
				if tags[3]==u'inf':
					taglist+=u'n'
					taglist+=u'----y'
				elif tags[3]==u'imp':
					taglist+=u'm'
					taglist+=person(tags[4])
					taglist+=number(tags[5])
					taglist+=u'-y'
				elif tags[3]==u'pres':
					taglist+=u'r'
					taglist+=person(tags[4])
					taglist+=number(tags[5])
					taglist+=u'-y'
				elif tags[3]==u'pii':
					taglist+=u'e'
					taglist+=person(tags[4])
					taglist+=number(tags[5])
					taglist+=u'-y'
				elif tags[3]==u'aor':
					taglist+=u'a'
					taglist+=person(tags[4])
					taglist+=number(tags[5])
					taglist+=u'-y'
				elif tags[3]==u'lp':
					taglist+=u'p'
					if tags[5] == u'du':
						continue
					else:
						taglist+=number(tags[5])
					taglist+=gender(tags[4])
					taglist+=u'y'	
				try:
					transitivity+=check_transitivity(tags[2])
				except:
					pass		
			else:	
				if tags[3]==u'inf':#<vblex><imperf><iv><inf>+hteti<vbmod><clt><futI><p1><sg>
					if len(tags)>4:
						if tags[4]=='+hteti':
							taglist+='f'
							taglist+=person(tags[8])
							taglist+=number(tags[9])
						else:
							continue
					else:
					  taglist+=u'n'
				elif tags[3]==u'imp':
					taglist+=u'm'
					taglist+=person(tags[4])
					taglist+=number(tags[5])
				elif tags[3]==u'pres':
					taglist+=u'r'
					taglist+=person(tags[4])
					taglist+=number(tags[5])
				elif tags[3]==u'pii':
					taglist+=u'e'
					taglist+=person(tags[4])
					taglist+=number(tags[5])
				elif tags[3]==u'aor':
					taglist+=u'a'
					taglist+=person(tags[4])
					taglist+=number(tags[5])
				elif tags[3]==u'lp':
					taglist+=u'p'
					taglist+=u'-'
					if tags[5] == u'du':
						continue
					else:
						taglist+=number(tags[5])
					try:
						taglist+=gender(tags[4])
					except:
						print sf,tags
						sys.exit()
				try:
					transitivity+=check_transitivity(tags[2])
				except:
					pass
	elif tags[0] == u'vbmod' or tags[0] == u'vbser':
		if tags[1]=='clt':
                        del tags[1]
                        taglist+=u'Va'
                else:
                        if tags[0]=='vbser':
                          taglist+='Va'
                        else:
                          taglist+='Vm'
		if tags[1]==u'inf':#<vblex><imperf><iv><inf>+hteti<vbmod><clt><futI><p1><sg>
			taglist+=u'n'
		elif tags[1]==u'imp':
			taglist+=u'm'
			taglist+=person(tags[2])
			taglist+=number(tags[3])
		elif tags[1]==u'pres':
			taglist+=u'r'
			taglist+=person(tags[2])
			taglist+=number(tags[3])
                elif tags[1]=='futII' and tags[2]=='pres':
                        taglist+=u'r'
                        taglist+=person(tags[3])
                        taglist+=number(tags[4])
		elif tags[1]=='futI':
		        taglist+='r'
		        taglist+=person(tags[2])
		        taglist+=number(tags[3])
		elif tags[1]==u'pii':
			taglist+=u'e'
			taglist+=person(tags[2])
			taglist+=number(tags[3])
		elif tags[1]==u'aor':
			taglist+=u'a'
			taglist+=person(tags[2])
			taglist+=number(tags[3])
		elif tags[1]==u'lp':
			taglist+=u'p'
			taglist+=u'-'
			if tags[3] == u'du':
				continue
			else:
				taglist+=number(tags[3])
			taglist+=gender(tags[2])
		try:
			transitivity+=check_transitivity(tags[2])
		except:
			pass
	elif tags[0] == u'part' and tags[4] == u'clt':
		taglist+=u'Var'
		taglist+=person(tags[-2]) 
		taglist+=number(tags[-1])	
		taglist+=u'y'
		try:
			transitivity+=check_transitivity(tags[2])
		except:
			pass
	#pronoun tags
	if tags[0] == u'prn':
		taglist+=u'P'
		if tags[1] == u'pers':
			taglist+=u'p'
			if tags[2] == u'clt':
				taglist+=person(tags[3])
				taglist+=gender(tags[4])
				taglist+=number(tags[5])
				taglist+=case(tags[6])
				#taglist+=u'--y-n'
			elif tags[2] != u'clt':
				taglist+=person(tags[2])
				taglist+=gender(tags[3])
				taglist+=number(tags[4])
				taglist+=case(tags[5])
				#taglist+=u'--n-n'
			if tags[5] == u'acc' and tags[4] == u'sg':
				if tags[3] == u'ma':
					taglist+=u'y'
				elif tags[3] == u'mi':
					taglist+=u'n'	
		elif tags[1] == u'dem':
			taglist+=u'd'
			taglist+=u'-'
			taglist+=gender(tags[2])
			taglist+=number(tags[3])
			taglist+=case(tags[4])		
			#taglist+=u'--n-a'
			if tags[4] == u'acc' and tags[3] == u'sg':
				if tags[2] == u'ma':
					taglist+=u'y'
				elif tags[2] == u'mi':
					taglist+=u'n'	
		elif tags[1] == u'pos':
			taglist+=u's'
			taglist+=person(tags[2])
			taglist+=gender(tags[3])
			taglist+=number(tags[4])
			taglist+=case(tags[5])
			"""if lf == u'moj' or lf == u'tvoj':
				taglist+=u's-n-a'
			elif lf == u'njegov':
				taglist+=u'smn-a'
			elif lf == u'njen' or lf == u'njezin':
				taglist+=u'sfn-a'
			elif lf == u'naš' or lf == u'vaš' or lf == u'njihov':
				taglist+=u'p-n-a'"""
			if tags[5] == u'acc' and tags[4] == u'sg':
				if tags[3] == u'ma':
					taglist+=u'y'
				elif tags[3] == u'mi':
					taglist+=u'n'				
		elif tags[1] == u'ref':
			taglist+=u'x'
			taglist+=u'-'
			if u'clt' not in tags:
				taglist+=gender(tags[3])
				taglist+=number(tags[4])
				taglist+=case(tags[5])	
				"""if lf == u'sebe':
					if len(sf) == 2:
						taglist+=u'--ypn'
					else:
						taglist+=u'--npn'
				else:
					taglist+=u'--nsa'"""			
				if tags[5] == u'acc' and tags[4] == u'sg':
					if tags[3] == u'ma':
						taglist+=u'y'
					elif tags[3] == u'mi':
						taglist+=u'n'								
			elif u'clt' in tags:
				taglist+=gender(tags[4])
				taglist+=number(tags[5])
				taglist+=case(tags[6])	
				"""if lf == u'sebe':
					if len(sf) == 2:
						taglist+=u'--ypn'
					else:
						taglist+=u'--npn'
				else:
					taglist+=u'--nsa'"""			
				if tags[6] == u'acc' and tags[5] == u'sg':
					if tags[3] == u'ma':
						taglist+=u'y'
					elif tags[3] == u'mi':
						taglist+=u'n'	
		elif tags[1] == u'itg':
			taglist+=u'q'
			if len(tags) > 2:
				if lf == u'tko':
					taglist+=u'3m-'
					taglist+=case(tags[4])
				elif lf == u'što':
					taglist+=u'3n-'
					taglist+=case(tags[4])
				else:
					taglist+=u'-'+gender(tags[2])
					taglist+=number(tags[3])
					taglist+=case(tags[4])
					if tags[4] == u'acc' and tags[3] == u'sg':
						if tags[2] == u'ma':
							taglist+=u'y'
						elif tags[2] == u'mi':
							taglist+=u'n'
		elif tags[1] == u'ind' or tags[1] == u'neg' or tags[1] == u'rel' or tags[1] == u'tot':
			taglist+=u'i'
			if len(tags) > 2:
				if lf in [u'što', u'šta', u'ništa', u'nešto', u'svašta', u'ništa', u'nešto', u'išta', u'štošta']:
					taglist+=u'3n-'
					taglist+=case(tags[4])
					#taglist+=u'--n-nn'
				elif lf in [u'tko', u'nitko', u'netko', u'svatko', u'svatko', u'nitko', u'netko', u'itko']:
					taglist+=u'3m-'
					taglist+=case(tags[4])
					#taglist+=u'--n-ny'
				elif lf == u'sve':
					taglist+=u'-'
					if gender(tags[2]) == u'-':
						taglist+=u'm'+number(tags[3])+case(tags[4])
						taglist2+=u'Pi-f'+number(tags[3])+case(tags[4])			
						taglist3+=u'Pi-n'+number(tags[3])+case(tags[4])			
					else:
						taglist+=gender(tags[2])
						taglist+=number(tags[3])
						taglist+=case(tags[4])
						#taglist+=u'----a'
				else:	
					taglist+=u'-'+gender(tags[2])
					taglist+=number(tags[3])
					taglist+=case(tags[4])
					#taglist+=u'--n-a'
					if tags[4] == u'acc' and tags[3] == u'sg':
						if tags[2] == u'ma':
							taglist+=u'y'
						elif tags[2] == u'mi':
							taglist+=u'n'
			else:
				taglist+=u'---'			
	
	#preposition tags
	if tags[0] == u'pr':
		taglist+=u'S'
		taglist+=case(tags[1])
	
	#conjunction tags
	if tags[0] == u'cnjcoo':
		taglist+=u'Cc'
	elif tags[0] == u'cnjsub':
		taglist+=u'Cs'
	
	#numeral tags
	if tags[0] == u'num':
		taglist+=u'M'
		if len(tags) == 1:
			if lf[-1].lower() in u'ivx':
				taglist+=u'r'
			else:
				taglist+=is_number(sf)			
		elif len(tags)==2:
		  taglist+=is_number(sf)
		  if tags[1]=='coll':
		    taglist+='s'
                  else:
                    taglist+='c'
		else:
			taglist+=is_number(sf)
			if tags[1] == u'ord':
				taglist+=u'o'
				if True:#len(tags) >2:
					taglist+=gender(tags[2])
					taglist+=number(tags[3])
					taglist+=case(tags[4])
					if tags[4] == u'acc' and tags[3] == u'sg':
						if tags[2] == u'ma':
							taglist+=u'y'
						elif tags[2] == u'mi':
							taglist+=u'n'												
			elif tags[1] != u'ord' and tags[1] != u'coll':#cardinal
				if len(tags)==4:
				  taglist+=u'c'
	  			  if tags[1]=='mfn':
	  			    taglist+='-'
                                  else:
                                    taglist+=gender(tags[1])
	  			  if tags[2]=='sp':
	  			    taglist+='-'
                                  else:
                                    taglist+=number(tags[2])
                                  taglist+=case(tags[3])
                                  if tags[3] == u'acc' and tags[2] == u'sg':
				    if tags[1] == u'ma':
				      taglist+=u'y'
				    elif tags[1] == u'mi':
                                      taglist+=u'n'	
                                #else:
                                #  continue
			elif tags[1] == u'coll':
				taglist+=u's'	#upitnik? novi tag? kolektivni? štaa? special?
				taglist+=gender(tags[2])
				taglist+='-'
				taglist+=case(tags[3])
				if tags[3] == u'acc' and tags[2] == u'sg':
					if tags[2] == u'ma':
						taglist+=u'y'
					elif tags[2] == u'mi':
						taglist+=u'n'	
	
	if tags[0] in [u'ma',u'mi',u'f',u'nt']:
		taglist+=u'Agp'
		taglist+=gender(tags[0])
		taglist+=number(tags[1])
		taglist+=case(tags[2])
		taglist+=u'y'

	if len(taglist) >1:
		if taglist[0] == u'V' or taglist[:2] == u'Ap':
			if (lf,sf,taglist) not in trans_hash:
				trans_hash[(lf,sf,taglist)]=set(transitivity)
			elif (lf,sf,taglist) in trans_hash:
				trans_hash[(lf,sf,taglist)].add(transitivity)	

	end()

sys.stderr.write(datetime.now().isoformat()+' read all\n')

#print lexiconin
#print lexiconout
"""
sys.stderr.write(datetime.now().isoformat()+' preprocessing adjective definiteness\n')	
#preprocessing adjective tags for definiteness
#this is magic beyond my capabilities of understanding, plain simple solution below 
for lema in lexiconin:
	for surface in lexiconin[lema]:
		for listtags in lexiconin[lema][surface]:
			for listtags2 in lexiconin[lema][surface]:
				if set.difference(set(listtags),set(listtags2)) == set([u'def']) or set.difference(set(listtags),set(listtags2)) == set([u'ind']):
					try:
						lexiconin[lema][surface][lexiconin[lema][surface].index(listtags2)].remove(u'ind')
						lexiconin[lema][surface][lexiconin[lema][surface].index(listtags)].remove(u'def')
					except:
						break
					try:
						lexiconin[lema][surface][lexiconin[lema][surface].index(listtags2)].remove(u'def')
						lexiconin[lema][surface][lexiconin[lema][surface].index(listtags)].remove(u'ind')
					except:
						break			
		
"""
sys.stderr.write(datetime.now().isoformat()+' mapping adjective tags\n')
#mapping adjective tags
#whuteva, it's simple, indefinite forms have to be deleted when the lemma and surface are
#identical and all tags are identical, but the definiteness, changed tag lists to tag sets
for lema in lexiconin:
	for surface in lexiconin[lema]:
	        #for tags in list(lexiconin[lema][surface]):
	        #  if tags[-1]=='ind' and tags[:-1]+('def',) in lexiconin[lema][surface]:
	        #    print lema,surface,tags
	        #    lexiconin[lema][surface].remove(tags)
		for tags in lexiconin[lema][surface]:
#			print lema,surface,tags
			taglist=u''
			if tags[0] == u'adj':			
				if len(tags) == 4:
					taglist+=u'Agp'
					taglist+=gender(tags[1])
					taglist+=number(tags[2])
					taglist+=case(tags[3])
					taglist+='y'
					if tags[3] == u'acc' and tags[2] == u'sg':
						if tags[1] == u'ma':
							taglist+=u'y'
						elif tags[1] == u'mi':
							taglist+=u'n'
				else:
					taglist+=u'Ag'
					if tags[1] == u'pst':
						taglist+=u'p'
					elif tags[1] == u'comp':
						taglist+=u'c'
					elif tags[1] == u'sup':
						taglist+=u's'
					elif tags[1] == u'ssup':
						#idi dalje ćao đaci #do not agree
						taglist+='p'
					taglist+=gender(tags[2])
					taglist+=number(tags[3])
					taglist+=case(tags[4])
					if tags[-1] == u'def':
						taglist+=u'y'
					elif tags[-1] == u'ind':
						taglist+=u'n'
                                        else:
                                                taglist+='y'
					#if tags [5] ==	u'def>' or u'indef>' videt kaj tu s definitessom tipa povući pickle leksikon i videt za taj surface form kakvo je stanje s definitessom i ako hm... ako ima i indefinite i definite onda staviti definite, a ako ima samo jedno od toga onda staviti to
					#znači niš, moram na kraj s tim, ne? ako je (.+)(y|n)* > \1(y|n)\2
					#dok gledamo pridjeve, znači prvi tag je adj [tagovi međusobno različiti]
					#možda postoji par di jedino po čemu se razlikuju je zadnji tag, odnosno definiteness				
					#
					#for lemma in lexiconin:
					#	for surface in lexiconin[lemma]:
					#		candidates=[]
					#		for tag in lexiconin[lemma][surface]:
					#			if tag[0] == u'adj':
					#				candidates.append[tag]
					#			for member in candidates:
					#				if set.difference(tag,member)== u'def' or u'ind':
					#					continue
					#				else:
					#					napravi novi tag valjda?
					#				candidates.append((len(set.intersection(set(t_expanded), set(tags))),t_expanded))			
									#AKO ISTI SURFACE FORM MOŽE BITI I DEFINITE I INDEFINITE ONDA NIŠTA; AKO JE SAMO JEDNO OD TOGA, ONDA DODAJ DEFINITENESS; meaning, ako nema intersectiona odnosno ako ima, ali u njemu definiteness nije issue, onda samo vrati tag kak je; ako 
					
					if tags[4] == u'acc' and tags[3] == u'sg':
						if tags[2] == u'ma':
							taglist+=u'y'
						elif tags[2] == u'mi':
							taglist+=u'n'
							
			elif tags[0] == u'n' and len(tags) > 5:
				taglist+=u'Asp'
				taglist+=gender(tags[4])
				taglist+=number(tags[5])
				taglist+=case(tags[6])
				if tags[-1] == u'def':
					taglist+=u'y'
				elif tags[-1] == u'ind':
					taglist+=u'n'				
				if tags[6] == u'acc' and tags[5] == u'sg':
					if tags[4] == u'ma':
						taglist+=u'y'
					elif tags[4] == u'mi':
						taglist+=u'n'	
			
			elif tags[0] == u'np' and tags[1] != u'acr' and len(tags) > 5:
				taglist+=u'Asp'
				taglist+=gender(tags[5])
				taglist+=number(tags[6])
				taglist+=case(tags[7])
				if tags[-1] == u'def':
					taglist+=u'y'
				elif tags[-1] == u'ind':
					taglist+=u'n'				
				if tags[7] == u'acc' and tags[6] == u'sg':
					if tags[5] == u'ma':
						taglist+=u'y'
					elif tags[5] == u'mi':
						taglist+=u'n'			
			
			elif tags[0] == u'np' and tags[1] == u'acr' and len(tags) > 5:
				taglist+=u'Asp'
				taglist+=gender(tags[4])
				taglist+=number(tags[5])
				taglist+=case(tags[6])
				if tags[-1] == u'def':
					taglist+=u'y'
				elif tags[-1] == u'ind':
					taglist+=u'n'				
				if tags[6] == u'acc' and tags[5] == u'sg':
					if tags[4] == u'ma':
						taglist+=u'y'
					elif tags[4] == u'mi':
						taglist+=u'n'

			if lema not in lexiconout:
				lexiconout[lema]={surface:set([taglist])}
			elif surface not in lexiconout[lema]:
				lexiconout[lema][surface]=set([taglist])
			elif taglist not in lexiconout[lema][surface]:
				lexiconout[lema][surface].add(taglist)

for lema in lexiconout:
  for surface in lexiconout[lema]:
    for tag in list(lexiconout[lema][surface]):
      if len(tag)>6:
        if tag[0]=='A':
          #print tag,lema,surface
          if tag[6]=='n' and tag[:6]+'y'+tag[7:] in lexiconout[lema][surface]:
            lexiconout[lema][surface].remove(tag)

#head -1657 expansion.hr | grep -c ' '
# head -1657 /home/filip/Apertium/apertium-hbs/expansion.hr | python transtag.ap-me.py | wc -l	
# filip@filip-Inspiron-5720:~/Apertium/scripts$ grep '<prn>' /home/filip/Apertium/apertium-hbs/expansion.hr | python transtag.ap-me.py | less
# filip@filip-Inspiron-5720:~/Apertium/apertium-hbs$ grep '<prn' expansion.hr | grep 'ref' | less

#print lexiconin
#print lexiconout
sys.stderr.write(datetime.now().isoformat()+' started output\n')
sys.stdout.write('s\tsa\tSg\n')
sys.stdout.write('s\tsa\tSl\n')

for lf in lexiconout:
	for sf in lexiconout[lf]:	
		for taglist in lexiconout[lf][sf]:
			if taglist != u'':
				if (lf,sf,taglist) in trans_hash:
					if trans_hash[(lf,sf,taglist)] != set([u'']):
						trans=u''.join(sorted(list(trans_hash[(lf,sf,taglist)])))
						sys.stdout.write(sf+u'\t'+lf+u'\t'+taglist+u'\t'+trans+u'\n')
					else:
						sys.stdout.write(sf+u'\t'+lf+u'\t'+taglist+u'\n')
				else:
					sys.stdout.write(sf+u'\t'+lf+u'\t'+taglist+u'\n')

sys.stderr.write(datetime.now().isoformat()+' output all\n')
"""						
	
	sys.stdout.write(i.strip()+u'\t^{0}/{1}{2}$\n'.format(sf, lf, u"".join(taglist)))

    
# head -20 /home/filip/Prompsit/SETimes/setimes.hr.v1.conllx | python transtag.py
"""
"""
for i in sys.stdin:
  fields = i.split(u'\t')
  if len(fields) > 1 and fields[1] == u'.':
    sys.stdout.write(u'^./.<sent>$\n')
  else:
    sys.stdout.write(i)
"""

# filip@filip-Inspiron-5720:~/Apertium/apertium-hbs$ lt-proc hbs.automorf.bin 

"""
and lf in [u'ja', u'ti', u'mi', u'vi', u'on'] and tags[5] in [u'g', u'd', u'a']:
				taglist.append(u'<pers><clt>')
			elif tags[1] == u'p':
"""			

"""
				if lm[-3:-1] == u'št' or lm[-3:] == u'tko':
				taglist+=u'3'
				taglist+=gender(tags[2])
				taglist+=u'-'+case(tags[4])
				taglist+=u'--n-n'
				if tags[2] == u'ma':
						taglist+=u'y'
				elif tags[2] == u'mi':
						taglist+=u'n'
"""
