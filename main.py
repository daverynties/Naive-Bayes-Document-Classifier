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

# baseball = Counter(class_word_prob['baseball'])
# space = Counter(class_word_prob['space'])
# medicine = Counter(class_word_prob['medicine'])
#
# list_unique = [a for a in baseball+medicine if (a not in baseball) or (a not in medicine)]

#convert list to dictionary to remove duplicate words and get count
for key in class_word_prob:
    #class_word_prob[key] = set(list(class_word_prob[key]))
    class_word_prob[key] = Counter(class_word_prob[key])



    
#calc probability function      
def calculateProbability(cls, word, found):
    
    vocabLength = len(Vocabulary)
    wordOccurance = class_word_prob[cls][word]
    classLength = len(class_word_prob[cls])
    
    #calculate Probability
    if found:
        probability = ((wordOccurance + 1) / (float(classLength) + vocabLength))
    else:
        probability = (1 / (float(classLength) + vocabLength))
    return log(probability)

#for every word in vocabulary, check occurances of each class and set value 
#of current dictionary
# for word in Vocabulary:
#     for cls in class_word_prob:
#         if word in class_word_prob[cls]:
#             class_word_prob[cls][word] = calculateProbability(cls, word)
#
# for cls in class_word_prob:
#     for word in class_word_prob[cls]:
#
            
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
        max_sum_class = -10000000.00

        for cls in class_word_prob:
            word_probability_values = []
            for word in testData:
                if word in class_word_prob[cls]:
                    x = calculateProbability(cls, word, True)
                    #print word, x
                    word_probability_values.append(x)
                else:
                    x = calculateProbability(cls, word, False)
                    word_probability_values.append(x)

            total_class_summation = sum(word_probability_values)

            if total_class_summation > max_sum_class:
                max_sum_class = total_class_summation
                class_word = cls

        if cls_value == class_word:    
            correct_classification.append("TRUE")
        else:
            correct_classification.append("FALSE")
    #correct_classification = list(set(correct_classification))

    total_values = len(correct_classification)
    #print(total_values)
    final_prediction = Counter(correct_classification)
    total_true = final_prediction.get('TRUE')
    total_false = final_prediction.get('FALSE')
    #print(total_true)
    #print total_false
    #print final_prediction

    accuracy_value = (float(total_true) / total_values)
    #print(accuracy_value)

print("\nClassification Accuracy: %.2f%%" % (round(accuracy_value, 4) * 100))

           



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
    
    
        
