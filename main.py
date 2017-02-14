from collections import defaultdict
from collections import Counter
from itertools import chain
from math import log
import numpy as np
import matplotlib.pyplot as plt
import datetime

plt.rcdefaults()

#==============================================================================
# ###_TRAINING_###
#==============================================================================
totalTrainingDocs = 0

unique_full_words = []
miss_class = []
correct_classification = []
guess_classification = []
incorrect_classification = []

class_word_prob = defaultdict(list)
class_doc_length = defaultdict(int)
vocabDicts = {}
class_word = 'test'

max_sum_class = -10000.00

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

with open('trainingData.txt') as f:
    for line in f.readlines():
        class_doc_length[(line.split(' ', 1)[0])] += 1
        data = line.split()
        class_word_prob[data[0]].extend(data[1:])
        totalTrainingDocs += 1
             
#get total unique words in all documents -- Vocabulary        
Vocabulary = list(set(list(chain.from_iterable(class_word_prob.values()))))

start_time = datetime.datetime.now()
#convert list to dictionary to remove duplicate words and get count
for key in class_word_prob:
    #class_word_prob[key] = set(list(class_word_prob[key]))
    class_word_prob[key] = Counter(class_word_prob[key])

for cls in class_doc_length:
    vocabDicts[cls] = Counter(Vocabulary)
    vocabDicts[cls] = merge_two_dicts(vocabDicts[cls], class_word_prob[cls])

#calc probability function      
def calculateProbability(cls, word):
    
    vocabLength = len(Vocabulary)
    wordOccurance = class_word_prob[cls][word]
    classLength = len(class_word_prob[cls])

    #calculate Probability
    probability = ((wordOccurance + 1) / (float(classLength) + vocabLength))
    return probability

def classValueCalculation(list):
    product = 0
    for x in list:
        x = log(x)
        product += x
    return product

#==============================================================================
###_CLASSIFICATION__###
#==============================================================================

test_class_word_prob = defaultdict(list)

with open('testData.txt') as f:
    for line in f.readlines():
        #class_doc_length[(line.split(' ', 1)[0])] += 1
        testData = line.split()
        #grab first word for future comparison
        cls_value = testData.pop(0)
        #loop through classes for each word
        max_sum_class = -10000.00

        for cls in vocabDicts:
            word_probability_values = []
            for word in testData:
                x = calculateProbability(cls, word)
                word_probability_values.append(x)

            prior_probability = (float(class_doc_length[cls]) / totalTrainingDocs)
            word_probability_values.insert(0, prior_probability)

            total_class_summation = classValueCalculation(word_probability_values)

            if total_class_summation > max_sum_class:
                max_sum_class = total_class_summation
                class_word = cls

        if cls_value == class_word:
            correct_classification.append("TRUE")
        else:
            correct_classification.append("FALSE")
            miss_class.append('G: {} --> A: {}'.format(class_word, cls_value))

    total_values = len(correct_classification)
    final_prediction = Counter(correct_classification)
    total_true = final_prediction.get('TRUE')
    total_false = final_prediction.get('FALSE')
    miss_class = Counter(miss_class)
    accuracy_value = (float(total_true) / total_values)
    total_time = datetime.datetime.now() - start_time

    milli = int(total_time.total_seconds() * 1000)

    print("\nClassification Accuracy: %.2f%%" % (round(accuracy_value, 4) * 100))
    print('Execution Time: %i Milliseconds' % milli)


