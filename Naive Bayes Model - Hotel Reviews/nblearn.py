import string
import math
import os.path
import re
import sys
import json

outputCounter = dict()

categoryCounter = dict()
categoryCounter["deceptive"]=0
categoryCounter["truthful"]=1
categoryCounter["positive"]=2
categoryCounter["negative"]=3

def getGIndex(genuiness):
    global categoryCounter
    return categoryCounter[genuiness]

def getSIndex(sentiment):
    global categoryCounter
    return categoryCounter[sentiment]

class HotelReview(object):
    """docstring for HotelReview"""
    def __init__(self, id, review):
        self.id = id
        self.review = review
        self.genuiness = None
        self.sentiment = None

    def fillTrainLabels(self, genuiness, sentiment):
        self.genuiness = genuiness
        self.sentiment = sentiment   
        
#counting the priors - from label file
freq = {}
freq1 = dict()
freq2 = dict()

doc = open('train-labels1.txt', 'r')
text_str = doc.read().lower()
match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_str)

for word in match_pattern:
    count = freq.get(word, 0)
    freq[word] = count + 1

summ1 = float(freq['truthful']+freq['deceptive'])
summ2 = float(freq['positive']+freq['negative'])
freq1['truthful']=math.log(freq['truthful']/summ1)
freq1['deceptive']=math.log(freq['deceptive']/summ1)

freq2['positive']=math.log(freq['positive']/summ2)
freq2['negative']=math.log(freq['negative']/summ2)


#splitting words and creating a dictionary
hotelReviewDictionary=dict()
with open('train-labels1.txt','r') as file1, open('train-text1.txt','r') as file2:
    for line in file2:
        index = line.find(' ')
        id = line[:index]
        rev = line[index:].strip()
        hotelReviewDictionary[id]=HotelReview(id,rev)

    for line in file1:
        wordlist = line.rsplit()
        id = wordlist[0]
        label1 = wordlist[1]
        label2 = wordlist[2]
        hotelReviewDictionary[id].fillTrainLabels(label1, label2)

for id, hotelReviewModel in hotelReviewDictionary.iteritems():
    for word in hotelReviewModel.review.split():
        if word in outputCounter:
            indexG = getGIndex(hotelReviewModel.genuiness)
            indexS = getSIndex(hotelReviewModel.sentiment)
            outputCounter[word][indexG] = outputCounter[word][indexG]+1
            outputCounter[word][indexS] = outputCounter[word][indexS]+1

        else:
            outputCounter[word] = {0:0,1:0,2:0,3:0}
            indexG = getGIndex(hotelReviewModel.genuiness)
            indexS = getSIndex(hotelReviewModel.sentiment)
            outputCounter[word][indexG] = outputCounter[word][indexG]+1
            outputCounter[word][indexS] = outputCounter[word][indexS]+1

count =[0,0,0,0]
for key,value in outputCounter.iteritems():
    for i in range(0,4):
        count[i] += outputCounter[key][i]

#print count
vocab = len(outputCounter)

count_prob = dict()

for key, val in outputCounter.iteritems():
    lst_prob=[0.0,0.0,0.0,0.0]
    for i in range(0,4):
       lst_prob[i] = math.log((outputCounter[key][i]+1)/float(count[i]+vocab))
    count_prob[key]= lst_prob
#print count_prob

#write model to file
file = open('nbmodel.txt','w')
for k,v in freq1.items():
    line = '{}, {}\n'.format(k, v)
    file.write(line)
for k,v in freq2.items():
    line = '{}, {}\n'.format(k, v)
    file.write(line)

file = open('nbmodel.txt','a')
json.dump(count_prob,file)
file.close()