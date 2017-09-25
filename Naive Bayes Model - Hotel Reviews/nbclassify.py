import string
import math
import os.path
import re
import sys
import json

categoryCounter = dict()
categoryCounter["deceptive"]=0
categoryCounter["truthful"]=1
categoryCounter["positive"]=2
categoryCounter["negative"]=3

freq1 =dict()
freq2 = dict()
file = open('nbmodel.txt', 'r')
l = file.readlines()
for i in range(0,2):
	c = l[i].split(',')
	cl,lg = c[0],c[1]
	freq1[cl] = float(lg)
for i in range(2,4):
	c = l[i].split(',')
	cl,lg = c[0],c[1]
	freq2[cl] = float(lg)
n = len(l)
count_prob = json.loads(l[4])
file.close()

hotelReviewDict = dict()
with open('train-text.txt','r') as file:
    for line in file:
        index = line.find(' ')
        id = line[:index]
        rev = line[index:].strip()
        hotelReviewDict[id]= rev


file = open('nboutput.txt','w')
'''
json.dump(hotelReviewDict,file)
file.close()
'''

label = dict()
for k,v in hotelReviewDict.iteritems():
	g = dict()
	p = dict()
	wordlist = v.split()
	for key,val in freq1.iteritems():
		g[key] = val
		for word in wordlist:
			if word not in count_prob:
				continue
			g[key] += count_prob[word][categoryCounter[key]]
	label1 = max(g,key=g.get)
	for key,val in freq2.iteritems():
		p[key] = val
		for word in wordlist:
			if word not in count_prob:
				continue
			p[key] += count_prob[word][categoryCounter[key]]
	label2 = max(p,key=p.get)
	file.write(k+' '+label1+' '+label2+'\n')
file.close()

