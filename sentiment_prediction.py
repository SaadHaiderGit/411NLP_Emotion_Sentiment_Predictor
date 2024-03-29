#CIS 411 NLP Final Project

#This program was adapted for use from CIS 411 assignment 3; sense in this instance refers to the sentiment or emotion conveyed by a given text string
#This program is trained to learn the various sense of a word, then uses a variety of algorithms to determine the sense
#Each dataset is divided into five folds, with four used for training and one for test; this is done 5 times until all five folds have been tested.


#imports go here
import sys
import math
import string
import copy

CONST_SENSE_NUM = 6 #the number of anticipated senses for the training/test set

#the stop words skipped over some variations
stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 
'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 
'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 
'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 
'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 
'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 
'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 
'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 
'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

#used for DL calculations
def NBC(feature):
    '''Returns the probabilities for a sense given a feature, using Naive Bayes Classifier.'''
    p_s_given_f = []
    for i in range(len(sense_count)):
        if feature not in word_count[i]:
            word_count[i][feature] = 0
        p_f = (word_count[i][feature] + 1) / s_f_dem[i]         #p(F|S) --> [(count(feature) + 1) / (count(sense) + V)]
        p_s_given_f.append(p_f * sense_probs[i])                #p(S|F) --> p(F|S) * p(S)
    return p_s_given_f

#used for NBC calculations
def multiFeatureNBC(feature):
    p_f_given_s = []
    for i in range(len(sense_count)):
        if feature not in word_count[i]:
            word_count[i][feature] = 0
        p_f_given_s.append((word_count[i][feature] + 1) / s_f_dem[i])         #p(F|S) --> [(count(feature) + 1) / (count(sense) + V)]

    return p_f_given_s #returns the list of p(F|S) for each sense S

#calculates the probablity that a given feature does not indicate a given sense
#used for DL calculations
def notNBC(feature):
    p_ns_given_f = []
    for i in range(len(sense_count)):
        feature_not_in_s = 0
        not_s_count = 0
        for j in range(len(sense_count)):
            if i==j:
                continue
            if feature not in word_count[i]:
                word_count[i][feature] = 0
            feature_not_in_s = feature_not_in_s + (word_count[j][feature])  
            not_s_count = not_s_count + sense_count[j][1]         #p(F|S) --> [(count(feature) + 1) / (count(sense) + V)]

        p_f = feature_not_in_s +1 / (not_s_count +len(word_bank))        #p(F|S) --> [(count(feature) + 1) / (count(sense) + V)]
        p_ns_given_f.append(p_f * (1-sense_probs[i]))                     #p(S|F) --> p(F|S) * p(S)
    return p_ns_given_f



def DLScore(num, dem):
    '''Returns the DL score of a feature word, showing how effective it is in determining the sense.'''
    return abs( math.log2(num/dem) )



#Main Program
if __name__ == "__main__":


    #Get corpus, then find senses
    #target_file = "train.txt"      #was used for debugging
    target_file = sys.argv[1]
    file = open(target_file)
    txt = [line for line in file if line != "\n"]   #get the entire corpus
    instance_num = int(len(txt))                  #get the total number of instances

    sense = []                          #comb through the corpus to find each possible sense
    for i in range(instance_num):
        poss_sense = (txt[i].split(';'))[1]
        if poss_sense not in sense:
            sense.append(poss_sense)
        if len(sense) == CONST_SENSE_NUM:             #stop once all senses are found
            break


    #Split all corpus instances into 5 folds. Each round, four are used for training, and one for test, so that all five folds are tested.
    r = instance_num % 5        #remainder. Used to find the number of instances per fold
    if r == 0:                  #(if no remainder, change the value to balance the below equations, so that fold_num = last_fold_num)
        r = 5
    fold_num = int( ((instance_num) - r + 5) / 5)   #equal num. of instances split evenly amongst the first four folds
    last_fold_num = int(fold_num - 5 + r)           #remaining instances given to fifth fold

    folds = []
    for m in range(4):          #for first four folds, add the appropriate instance information needed to calculate sense
        folds.append([])        
        for i in range(fold_num):
            instance_index = (fold_num * m) + (i)   #find the index of the instances we are pulling from in the text
            instance_values = txt[instance_index].split(";")
            folds[m].append( (instance_values[0], instance_values[1]) )   #(only <answer instance...> and the actual sentence are needed for extraction purpose)
    
    folds.append([])            #for last fold, take the remaining instances and their info
    for i in range(last_fold_num):
        instance_index = (fold_num * 4) + (i)
        instance_values = txt[instance_index].split(";")
        folds[4].append( (instance_values[0], instance_values[1]) )       


    #----------------------------------------LOOP FOR USING FOLDS TO FIND WSD----------------------------------------
    overall_corr_predictions = 0 #used for DL variation
    overall_baseline_pred = 0 #used to get baseline
    overall_nbc_corr_pred = 0 #used for NBC variations

     #used to determine how often each sense is confused for another in a given fold
    sense_confusion = [{},{},{},{},{}]
    for fold in sense_confusion:
        for x in sense:
            fold[x] = {}
            for y in sense:
                fold[x][y]=0
    

    for m in range(5):  #each round a new fold becomes the test, and the rest are training; do this for 5 rounds so all folds are tested (with accuracy found for each)
        sense_count = [[x, 0] for x in sense]                   #counts for each individual sense
        total_sense_count = 0                                   #number of senses altogether
        if m == 4:                                              #(if last fold = test fold, subtract its instances from the total instances)
            total_sense_count = instance_num - last_fold_num
        else:                                                   #(else another fold = test fold; subtract its instances from the total instances)
            total_sense_count = instance_num - fold_num
        word_count = [{} for y in range(len(sense_count))]      #word counts correlate to each specific sense
        word_bank = []                                          #word bank contains all global words, regardless of sense

        #-----TRAIN-----
        for x in range(5):  #for each fold:
            if x == m:      #skip the test fold
                continue
            for s in range(len(folds[x])):
                curr_sense = folds[x][s][1]        #take the sense of each fold
                for i in range(len(sense_count)):
                    if curr_sense == sense_count[i][0]:                #then increase the count of that sense
                        sense_count[i][1] += 1
                        sentence = folds[x][s][0]                   #also gather the words of the sentence for that sense
                        for words in sentence.lower().split():
                            if words[0] in string.punctuation:              #(strip off beginning and ending punctuation, for accurate counts)
                                words = words[1:]
                                if words == "":
                                    continue
                            if words[-1] in string.punctuation:                             
                                words = words[:-1]
                                if words == "":
                                    continue
                            if words in stop_words: #removes stop words from sentence; commented out for variations that include stop words
                                continue

                            if words not in word_bank:
                                word_bank.append(words)
                            if words not in word_count[i]:                  #(if new word, add to dict; otherwise +1 to count)
                                word_count[i][words] = 1
                            else:
                                word_count[i][words] += 1
                        break;


        #apply Naive Bayes Model to find the DL score of each word and its correlated sense
        #(For this we create a list, then append to it each word with its score and appropriate tag)
        DL_list = []
        sense_probs = []
        s_f_dem = []                            #aka the demonimators for a feature-given-sense in Naive Bayes; w/ add-one smoothing, is (sense_count + sense vocab)
        for i in range(len(sense_count)):       #store the probability of each sense appearing, then the demonimators
            sense_probs.append(sense_count[i][1] / total_sense_count)
            s_f_dem.append(sense_count[i][1] + len(word_bank))

        for word in word_bank:
            f_given_s_probs = NBC(word)               #use Naive Bayes Classifier, then apply sense with higher prob. to the current word_
            f_not_s_probs = notNBC(word)
            probs_reverse_sorted = copy.deepcopy(f_given_s_probs)
            probs_reverse_sorted.sort()
            probs_reverse_sorted.reverse()

            DL_score_list = []
            for k in range(len(sense_count)):   #Finds the DL score for each sense for the feature
                DL_score_list.append(DLScore(f_not_s_probs[k],f_given_s_probs[k]))

            DL_score_list_sor = copy.deepcopy(DL_score_list)
            DL_score_list_sor.sort()
            
            DL_list.append([word, sense[DL_score_list.index(DL_score_list_sor[0])], DL_score_list_sor[0]]) #stores the sense with the lowest DL score (i.e. the word least likely to indicate a different sense)
           
        DL_list = sorted(DL_list, key = lambda x: -x[2])  
        DL_list.append(["<TIEBREAK \>", sense[f_given_s_probs.index(probs_reverse_sorted[0])], 0]) #if the DL_list fails to predict the sense, use the higher prob. sense as the tiebreaker)
           


        #-----TEST-----
        corr_predictions = 0
        nbc_corr_predictions = 0
        baseline_predictions = 0
        most_prob_sense = -1
        predictions = len(folds[m])         #the number of instances in the test fold = the number of predictions made 

        prob_tracker = 0
        for k in range(len(sense_count)):
            if sense_count[k][1] > prob_tracker:
                most_prob_sense = k
                prob_tracker = sense_count[k][1]

        for s in range(len(folds[m])):      #for each test fold instance, pull out its sentence and predict it with DL_list
            id = folds[m][s][0]
            ground_truth = folds[m][s][1]
            if sense[most_prob_sense] == ground_truth:
                baseline_predictions += 1
            sentence = folds[m][s][0].lower().split()
            probabilities = copy.deepcopy(sense_probs)
            for i, words in enumerate(sentence):

                if words[0] in string.punctuation:              #(strip off beginning and ending punctuation, for accurate predictions)
                    sentence[i] = words[1:]
                    if words == "":
                        continue
                if words[-1] in string.punctuation:                             
                    sentence[i] = words[:-1]
                
                if words in stop_words:     #ignores stop words in test set
                    continue

                p_f_s = multiFeatureNBC(words) #calculates the probability of each sense for the item in the test set based on its features
                for p in range(len(p_f_s)):
                    probabilities[p] *= p_f_s[p]

            #selects the highest probability as the sense of the sentence, checks accuracy of prediction
            max_arg = probabilities.index(max(probabilities))
            if sense[max_arg] == ground_truth:
                nbc_corr_predictions += 1

            else:
                sense_confusion[m][ground_truth][sense[max_arg]] += 1 #if prediction is incorrect, saves what sense it was confused for

            for i in DL_list:                                       #Predict the sentence sense based off of DL. Either a feature word is found, or a tiebreaker is needed.
                if i[0] in sentence or i[0] == "<TIEBREAK \>":
                    if i[1] == ground_truth:                        #If the feature's associated sense matches the ground truth, increment corr_predictions
                        corr_predictions += 1
                   
                    break;

        fold_acc = corr_predictions / predictions * 100 
        nbc_fold_acc = nbc_corr_predictions / predictions *100  
        baseline_acc = baseline_predictions / predictions * 100                      #output the fold's accuracy for DL and NBC
        print("DL accuracy of fold " + str(m+1) + ":", round(fold_acc, 1), "%") 
        print("NBC accuracy of fold " + str(m+1) + ":", round(nbc_fold_acc,1), "%")
        # for correct in sense_confusion[m].items(): #displays what senses were confused for others; uncomment to view
        #     for confused_for in correct:
        #         print(confused_for)
        #print("Baseline accuracy of fold "+ str(m+1) + ":", round(baseline_acc, 1), "%")    #displays baseline prediction accuracy
        overall_corr_predictions += corr_predictions                         #add up the number of correct predictions for later
        overall_baseline_pred += baseline_predictions
        overall_nbc_corr_pred += nbc_corr_predictions


    #The loop has ended. Find the total accuracy (and close the output).
    overall_fold_acc = overall_corr_predictions / instance_num * 100            #(instance_num is all of the instances tested in this file)
    overall_baseline_acc = overall_baseline_pred / instance_num *100
    overall_nbc_acc = overall_nbc_corr_pred / instance_num *100
    print("DL total accuracy:", round(overall_fold_acc, 1), "%")
    print("NBC total accuracy:", round(overall_nbc_acc, 1), "%")
    #print("Baseline accuracy:", round(overall_baseline_acc,1),"%")#displays baseline prediction accuracy

