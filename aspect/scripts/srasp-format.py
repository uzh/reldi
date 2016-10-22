# -*- coding: utf8 -*

# parses the old data set format (before lrec2016 submission e.g. "merged.txt") and produces a column-based format 
# usage: python srasp-format.py <old-datafile> 

import re
import codecs
import sys


infile = sys.argv[1]

readin = codecs.open(infile, "r", "utf-8")


vfid = 0							# initialise verb form ID  
bvid = 0							# initialise base verb ID
deriv = {}							# initialise the main data structure
bfreq = {}

for line in readin:
	line = re.sub(r'\n', '', line)					# instead of chomp in Perl
	if len(line) > 0:
		elements = line.split(' ')
		if len(elements[0]) > 1:
			basic = elements[0]
			bfreq[basic] = elements[1]
			deriv[basic] = []						# initialise the structure to relate the derivations with their corresponding base verb 
		#	print basic								#for checking
		elif len(elements) > 0:
			deriv[basic].append(elements)			# add the verb forms into the structure, line by line

for item in sorted(deriv):
	vfid += 1
	bvid = vfid										#increase the id of the main verb
	print vfid, item.encode('utf8'), bfreq[item], "I", "NO", "NO", "0"
	for i in range(len(deriv[item])):
		for j in range(len(deriv[item][i]) - 1):
			if deriv[item][i][j] != "-" and len(deriv[item][i][j]) > 2:
				vfid += 1
				print vfid, deriv[item][i][j].encode('utf8'), deriv[item][i][j+1], 
				if j == 1: 
					print "P", "YES", "NO",
				else:
					print "I", "YES", "YES",	
				print bvid			  
