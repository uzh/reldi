# -*- coding: utf8 -*

# counts the number of different items in the old data set format (before lrec2016 submission e.g. "merged.txt")
# usage: python srasp-count.py <old-datafile> 

import re
import codecs
import sys

"""
define input file 
"""
infile = sys.argv[1]

readin = codecs.open(infile, "r", "utf-8")

"""
reading the input data
"""

basic = ""
deriv = {} 		#nested dictionary
bfreq = {}		#frequency dictionary

for line in readin:
	line = re.sub(r'\n', '', line)					# instead of chomp in Perl
	if len(line) > 0:						# if line not empty
		elements = line.split(' ')				# turn the line into a list called "elements"
		if len(elements[0]) > 1:
			basic = elements[0]				# assign the verb to basic
			bfreq[basic] = elements[1]			# assgn the frequency of the verb
			deriv[basic] = []				# initialise a new list for all the derivations of basic
		#	print basic								#for checking
		elif len(elements) > 0:
			deriv[basic].append(elements)			# store all the elements in the derivation list, both verbs and their frequencies are appended in the same way 


"""
counting
"""

cbasic = 0								# initialise the count of base verbs
callderiv = {}								# initialise the main dict for counting
callderiv["short"] = 0							
callderiv["long"] = 0							

for item in sorted(deriv):	`					# go through the main dict where we stored the data while reading the file
#	print item.encode('utf8'), bfreq[item]				# for checking
	cbasic +=1							# increase the count of basic forms
	cderiv = 0							# initialise the counter for the number of derivations
	cpref = 100							# to count the number of lines in each matrix, these counts go into callderiv as keys and need to be distinguished from the total derivation counts which are also keys (1-26), so any key higher than 100 represent the number of lines in a matrix (e.g. 101 = one line, 102 = two lines and so on)
	print item.encode('utf8'), 					# comma puts the next printed item in the same line
	for item2 in deriv[item]:
		print item2, 
		print len(item2),
		if len(item2) < 5:
			callderiv["short"] +=1
		else:
			callderiv["long"] +=1
		for i in range(0, len(item2)):
			if item2[i] != "-" and item2[i] != "0":		# if the entry is a derivation (= has a value different from "-" and has non-zero frequency)
				cderiv += 1				# increase the count of derivations 
	cderiv = cderiv/2						# divide the sum by 2 because we increased the count for the frequency entries too
	cpref = cpref + len(deriv[item])				# add the number of derivations to the initialised number 100 for further processing
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
	
