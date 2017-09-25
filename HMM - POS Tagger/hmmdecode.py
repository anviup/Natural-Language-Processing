import math
import codecs
import json

transition = dict()
trans = dict()
emission = dict()
emm = dict()
tagCount = dict()
startTags = dict()
fWord = dict()
allTags = dict()

file1 = codecs.open("hmmmodel.txt", "r",'utf-8')
line = file1.readlines()
trans = json.loads(line[0])
startTags = json.loads(line[1])
emm = json.loads(line[2])
tagCount = json.loads(line[3])
tag = json.loads(line[4])
file1.close()

for k,v in trans.iteritems():
    k = str(k)
    index = k.find(",")
    a1 = k[index-3:index-1]
    a2 = k[index+4:index+6]
    tup = (a1, a2)
    transition[tup]= v

for k,v in emm.iteritems():
    k = str(k)
    index = k.find(",")
    a1 = k[3:index - 1]
    a2 = k[index + 4:index + 6]
    tup = (a1, a2)
    emission[tup] = v

def findMax(d,k,v):
    temp = dict()
    maxProb = list()
    maxProb.append("-1000")
    maxProb.append(" ")
    for key in d:
        tup = (key[1],k[1])
        xyz = (k[1],k[0])
        temp[xyz] = (float(transition[tup]) + float(v) + float(d[key]))
        if temp[xyz]>int(maxProb[0]):
            maxProb[0]= temp[xyz]
            maxProb[1] = key[1]
    tup = (k,maxProb)
    return tup

file2 = codecs.open(sys.argv[1], "r","utf-8")
while True:
    line = file2.readline()
    if ("" == line):
        break
    index = line.find(";")
    words = line[:index]
    words = words.split()
    first_word = words[0]
    wd = len(words)-1
    last_word = words[wd]

    viterbi = list()
    for key, val in startTags.iteritems():
        for k, v in emission.iteritems():
            tup = (first_word, key)
            if k == tup:
                prob = round(float(v) + float(val), 5)
                fWord[k] = prob
    viterbi.append(fWord)
    print viterbi

    lst = list()
    fin = list()
    for w in range(1, len(words)):
        allTags = {}
        for k, v in emission.iteritems():
            if words[w] == k[0]:
                allTags[k] = v
            if words[w]!= k[0]:
                for tag in tagCount:
                    tup = (words[w],tag)
                    allTags[tup] = 0
        viterbi.append(allTags)

    for i in range(1,len(viterbi)):
        lst = list()
        for key in viterbi[i]:
            lst.append(findMax(viterbi[i-1],key,viterbi[i][key]))
        fin.append(lst)

    temp = -1000
    fd = len(fin)-1
    for f in fin[fd]:
        temp = max(temp,f[1][0])

    for f in fin[fd]:
        if f[1][0]== temp:
            back = f[1][1]

    backList = list()
    for f in reversed(fin):
        for each in f:
            if each[0][0]==last_word and each[1][0]== temp:
                backList.append(back)
            else:
                if each[0][1]==back:
                    back = each[1][1]
                    backList.append(back)

    tagList = list()
    for tag in reversed(backList):
        tagList.append(tag)

    fileW = codecs.open("hmmoutput.txt", 'a',"utf-8")
    for i in range(len(words)):
        print words[i]
        fileW.write(words[i] + str("/") + tagList[i] + str(" "))
    fileW.write("\n")
    fileW.close()

file2.close()