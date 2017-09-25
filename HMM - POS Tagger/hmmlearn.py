from collections import defaultdict
import math
import codecs
import json

transition = defaultdict(int)
emission = defaultdict(int)
tag_count = defaultdict(int)
back_count = defaultdict(int)
countOfTag = 0

file = codecs.open(sys.argv[1],'r','utf-8')
while True:
    line = file.readline().strip("\n")
    each = line.split()
    back_ptr = 0
    for w in each:
        index = len(w)                #change here for finding only last two characters
        wrd = w[:index-3]
        tag = w[index-2:]

        back_count[back_ptr]+=1

        tup1=(back_ptr,tag)
        transition[tup1]+=1
        back_ptr = tag

        tup2=(wrd,tag)
        emission[tup2]+=1

        if tag not in tag_count:
            countOfTag+=1
        tag_count[tag] += 1

    if("" == line):
        break

transitionW = dict()
emissionW = dict()
start = dict()
start_count = dict()
sum =0

for k,v in transition.iteritems():
    if k[0]==0:
        start[k[1]]=v
        sum+=v

for k,v in start.iteritems():
    prob = math.log(float(v)/float(sum))
    start_count[k]= prob

for k1,v1 in transition.iteritems():
    for k2, v2 in back_count.iteritems():
        if k1[0]==k2 and k2!=0:
            transitionW[str(k1)]= math.log((float(v1+1))/(float(v2+countOfTag)))

for k1,v1 in back_count.iteritems():
    for k2,v2 in back_count.iteritems():
        if k1!=0 and k2!=0:
            tup=(k1,k2)
            if tup not in transition:
                transitionW[str(tup)]= math.log(1/(float(v2+countOfTag)))

for k1,v1 in emission.iteritems():
    for k2, v2 in tag_count.iteritems():
        if k1[1]==k2:
            emissionW[str(k1)]= math.log(float(v1)/float(v2))

fileW = codecs.open('hmmmodel.txt','w','utf-8')
json.dump(transitionW,fileW)
fileW.write("\n")
json.dump(start_count,fileW)
fileW.write("\n")
json.dump(emissionW,fileW)
fileW.write("\n")
json.dump(tag_count,fileW)
fileW.write("\n")
json.dump(countOfTag,fileW)
fileW.close()