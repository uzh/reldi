# -*- coding: utf8 -*

# merges two files with verbs sorted according to verb aspect 
# usage:  python merge-asp.py maja1-999.txt tanja1000-1230.txt > merged.txt

import re
import codecs
import sys


firstfile = sys.argv[1]
secondfile = sys.argv[2]

firstin = codecs.open(firstfile, "r", "utf-8")
secondin = codecs.open(secondfile, "r", "utf-8")

deriv = {}
basic = ""
bfreq = {}

for line in firstin:
	line = re.sub(r'\n', '', line)					# instead of chomp in Perl
	if len(line) > 0:
		elements = line.split('\t')
		if len(elements[0]) > 1:
			if re.match(r"\*", elements[0]):
				basic = re.sub("\*", "", elements[0])
				bfreq[basic] = 0
			else: 
				(basic, bfreq[basic]) = elements[0].split(' ')
			deriv[basic] = []
		#	print basic								#for checking
		elif len(elements) > 0:
			deriv[basic].append(elements)

for line2 in secondin:
	line = re.sub(r'\n', '', line2)					# instead of chomp in Perl
	if len(line) > 0:
		elements = line.split('\t')
		if len(elements[0]) > 1:
			if re.match(r"\*", elements[0]):
				basic = re.sub("\*", "", elements[0])
				if basic not in deriv:
					bfreq[basic] = 0
			else: 
				(basic, bfreq[basic]) = elements[0].split(' ')
			if basic not in deriv:
				deriv[basic] = []
		#	print basic								#for checking
		elif len(elements) > 0:
			deriv[basic].append(elements)



for item in sorted(deriv):
	print item.encode('utf8'), bfreq[item]
	for item2 in deriv[item]:
		for i in range(0, len(item2)):
			print item2[i].encode('utf8'),		
		print
	print		
		
