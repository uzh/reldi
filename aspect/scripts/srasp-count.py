# -*- coding: utf8 -*

# counts the number of different items in the old data set format (before lrec2016 submission e.g. "merged.txt")
# usage: python srasp-count.py <old-datafile> 

import re
import codecs
import sys


infile = sys.argv[1]

readin = codecs.open(infile, "r", "utf-8")

basic = ""
deriv = {}
bfreq = {}

for line in readin:
	line = re.sub(r'\n', '', line)					# instead of chomp in Perl
	if len(line) > 0:
		elements = line.split(' ')
		if len(elements[0]) > 1:
			basic = elements[0]
			bfreq[basic] = elements[1]
			deriv[basic] = []
		#	print basic								#for checking
		elif len(elements) > 0:
			deriv[basic].append(elements)
cbasic = 0
callderiv = {}
callderiv["short"] = 0
callderiv["long"] = 0

for item in sorted(deriv):
#	print item.encode('utf8'), bfreq[item]
	cbasic +=1
	cderiv = 0
	cpref = 100											#to count the number of lines in each matrix, these counts go into callderiv as keys and need to be distinguished from the total derivation counts which are also keys (1-26), so any key higher than 100 represent the number of lines in a matrix (e.g. 101 = one line, 102 = two lines and so on)
	print item.encode('utf8'), 
	for item2 in deriv[item]:
		print item2, 
		print len(item2),
		if len(item2) < 5:
			callderiv["short"] +=1
		else:
			callderiv["long"] +=1
		for i in range(0, len(item2)):
			if item2[i] != "-" and item2[i] != "0":
				cderiv += 1
	cderiv = cderiv/2
	cpref = cpref + len(deriv[item])
	print len(deriv[item]), cderiv	
	if cderiv in callderiv:
		callderiv[cderiv] +=1
	else:
		callderiv[cderiv] = 1 
	if cpref in callderiv:
		callderiv[cpref] += 1
	else:
		callderiv[cpref] = 1
	

print "N(base) = ", cbasic	

print "Number of derivations:"

for item3 in callderiv:
	print item3, callderiv[item3]
	
