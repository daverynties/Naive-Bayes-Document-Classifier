from collections import defaultdict
from collections import Counter
from itertools import chain
from math import log
import numpy as np
import matplotlib.pyplot as plt

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
    wordOccurance = vocabDicts[cls][word]
    classLength = len(class_word_prob[cls])
    
    #calculate Probability
<<<<<<< HEAD
    probability = ((wordOccurance + 1) / (float(classLength) + vocabLength))
    return probability
=======
   # if found:
    probability = ((wordOccurance + 1) / (float(classLength) + vocabLength))
   # else:
       # probability = (1 / (float(classLength) + vocabLength))
    return (probability)
>>>>>>> fd4157a2d2f9f1c03d66139c65a94474490f0a3f

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
<<<<<<< HEAD
                x = calculateProbability(cls, word)
                word_probability_values.append(x)
=======
                #if word in vocabDicts[cls]:
                x = calculateProbability(cls, word)
                    #print word, x
                word_probability_values.append(x)
               # else:
                  #  x = calculateProbability(cls, word, False)
                  #  word_probability_values.append(x)
>>>>>>> fd4157a2d2f9f1c03d66139c65a94474490f0a3f

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
<<<<<<< HEAD
            miss_class.append('G: {} --> A: {}'.format(class_word, cls_value))
=======
            incorrect_classification.append(class_word)
            guess_classification.append(cls_value)
            #print('Guess: ' + class_word + '\nClassification: ' + cls_value)
>>>>>>> fd4157a2d2f9f1c03d66139c65a94474490f0a3f

    total_values = len(correct_classification)
    final_prediction = Counter(correct_classification)
    total_true = final_prediction.get('TRUE')
    total_false = final_prediction.get('FALSE')
    miss_class = Counter(miss_class)

    for k, v in miss_class.items():
        if v < 30:
            del miss_class[k]

    labels, values = zip(*miss_class.items())

    accuracy_value = (float(total_true) / total_values)

    indexes = np.arange(len(labels))
    width = 1

    plt.tick_params(labelsize=10)
    plt.barh(indexes, values, width)
    plt.yticks(indexes + width * 0.5, labels)
    plt.show()

print("\nClassification Accuracy: %.2f%%" % (round(accuracy_value, 4) * 100))

