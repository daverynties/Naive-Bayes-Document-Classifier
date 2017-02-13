from collections import defaultdict
from collections import Counter
from itertools import chain
from math import log
#==============================================================================
# ###_TRAINING_###
#==============================================================================
totalTrainingDocs = 0
unique_full_words = []

class_word_prob = defaultdict(list)
class_doc_length = defaultdict(int)
vocabDicts = {}

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
   # if found:
    probability = ((wordOccurance + 1) / (float(classLength) + vocabLength))
   # else:
       # probability = (1 / (float(classLength) + vocabLength))
    return (probability)

def classValueCalculation(list):
    product = 0
    for x in list:
        x = log(x)
        product += x
    return product
            
#==============================================================================
###_CLASSIFICATION__###
#==============================================================================
class_word = 'test'
correct_classification = []
guess_classification = []
incorrect_classification = []
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

        for cls in vocabDicts:
            word_probability_values = []
            for word in testData:
                #if word in vocabDicts[cls]:
                x = calculateProbability(cls, word)
                    #print word, x
                word_probability_values.append(x)
               # else:
                  #  x = calculateProbability(cls, word, False)
                  #  word_probability_values.append(x)

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
            incorrect_classification.append(class_word)
            guess_classification.append(cls_value)
            #print('Guess: ' + class_word + '\nClassification: ' + cls_value)

    total_values = len(correct_classification)
    final_prediction = Counter(correct_classification)
    total_true = final_prediction.get('TRUE')
    total_false = final_prediction.get('FALSE')

    incorrect_classification = Counter(incorrect_classification)
    guess_classification = Counter(guess_classification)

    print'----------------------'
    print incorrect_classification
    print guess_classification
    print'----------------------'

    accuracy_value = (float(total_true) / total_values)
    #print(accuracy_value)

print("\nClassification Accuracy: %.2f%%" % (round(accuracy_value, 4) * 100))
