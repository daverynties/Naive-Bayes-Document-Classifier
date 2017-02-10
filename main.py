from collections import defaultdict
from collections import Counter
from itertools import chain

totalTrainingDocs = 0

d = defaultdict(list)
my_dict = defaultdict(int)
vocabDicts = {}

with open('trainingData.txt') as f:
    for line in f.readlines():
        my_dict[(line.split(' ', 1)[0])] += 1
        data = line.split()
        d[data[0]].extend(data[1:])
        totalTrainingDocs += 1
             
#get total unique words in all documents -- Vocabulary        
Vocabulary = list(set(list(chain.from_iterable(d.values()))))

#convert list to dictionary to remove duplicate words and get count
for key in d:
    d[key] = Counter(d[key])
    
#calc probability function      
def calculateProbability(cls, word):
    
    vocabLength = len(Vocabulary)
    wordOccurance = d[cls][word]
    classLength = len(d[cls])
    
    #calculate Probability
    probability = ((wordOccurance + 1) / (float(classLength) + vocabLength))    
    return probability
#for every word in vocabulary, check occurances of each class and set value 
#of current dictionary        
for word in Vocabulary:      
    for cls in d:
        if word in d[cls]:
            d[cls][word] = calculateProbability(cls, word)
            
    
