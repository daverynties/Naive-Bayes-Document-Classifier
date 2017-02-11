from collections import defaultdict
from collections import Counter
from itertools import chain
from math import log
#==============================================================================
# ###TRAINING
# 
#==============================================================================
totalTrainingDocs = 0

class_word_prob = defaultdict(list)
class_doc_length = defaultdict(int)
vocabDicts = {}

with open('trainingData.txt') as f:
    for line in f.readlines():
        class_doc_length[(line.split(' ', 1)[0])] += 1
        data = line.split()
        class_word_prob[data[0]].extend(data[1:])
        totalTrainingDocs += 1
             
#get total unique words in all documents -- Vocabulary        
Vocabulary = list(set(list(chain.from_iterable(class_word_prob.values()))))

#convert list to dictionary to remove duplicate words and get count
for key in class_word_prob:
    class_word_prob[key] = Counter(class_word_prob[key])
    
#calc probability function      
def calculateProbability(cls, word):
    
    vocabLength = len(Vocabulary)
    wordOccurance = class_word_prob[cls][word]
    classLength = len(class_word_prob[cls])
    
    #calculate Probability
    probability = ((wordOccurance + 1) / (float(classLength) + vocabLength))    
    return probability
#for every word in vocabulary, check occurances of each class and set value 
#of current dictionary        
for word in Vocabulary:      
    for cls in class_word_prob:
        if word in class_word_prob[cls]:
            class_word_prob[cls][word] = calculateProbability(cls, word)
            
#==============================================================================
# ###_CLASSIFICATION__###
# 
#==============================================================================
class_word = 'test'
correct_classification = []
max_sum_class = -10000000.00

test_class_word_prob = defaultdict(list)

with open('testData.txt') as f:
    for line in f.readlines():      
        #class_doc_length[(line.split(' ', 1)[0])] += 1
        testData = line.split()
        #grab first word for future comparison
        cls_value = testData.pop(0)
        #loop through classes for each word
        for cls in class_word_prob:
            word_probability_values = []
            for word in testData:
                if word in class_word_prob[cls]:
                     word_probability_values.append(log(class_word_prob[cls][word]))
                     print("true")
                else:
                    word_probability_values.append(log(1 / float(class_doc_length[cls])))
            if sum(word_probability_values) > max_sum_class:
                max_sum_class = sum(word_probability_values)
                class_word = cls
    if cls_value == class_word:    
        correct_classification.append("TRUE")
    else:
        correct_classification.append("FALSE")
    #correct_classification = list(set(correct_classification))
        
           



#create nested dic of test docs to get unique words and count
#count will be overrided to probability value for each class
    #for each class
        #for each word in test doc
        #get first word for class validation
            #if word in class
                #get probability value and append to dict[class][word] value
            #else
                #probability value =  (float(1 / len(totalTrainingDocs)))
                #log(probability value)
                #append value to list
        #get sum of all values in list
        #if list summation is greater than previous
            #class_top_value = new value
            #class_prediction = new value
    #if class_prediction = first_word
        #correct_prediction + 1
    #else
        #incorrect_prediction + 1
    
    
        
