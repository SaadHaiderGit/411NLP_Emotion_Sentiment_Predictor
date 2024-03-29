# Emotion Sentiment Predictor

This is the source code for a emotion sentiment predictor, made in Python for CIS 411: Intro to NLP. It comes with a corpus gained from the Huggingface Emotion dataset, which is a collection of English Twitter messages. The code will take an inputted text file and read the corpus one line at a time, and for each line, it will determine a corresponding emotion. There are six different emotions it will choose for classification: joy, sadness, anger, fear, surprise, and love.

The Emotion Sentiment Predicator uses no libaries and instead has an NLP model made from scratch for this specific task, using a Naive Bayes Classifier system. It also has a Decision List system for posterity; this was an older model that was primarily used for the system before being replaced. The data is divided into five folds, with four for training and one for testing; the model has five rounds where a new fold is used for testing (and the rest for training), until all folds have been used. The average accuracy is calculated this way.

Our model has an overall accuracy of 63.8% for the Naive Bayes Classifier, when used on our corpus. (For Decision List, it is 35.4%.)

The provided code can be used to run the model and display results on accuracy. You can take the github link and clone it to your local repo. To run the program, open it in the terminal and add a system argument for the desired text file you wish to use. (This repo comes with a train.txt file, which contains the cleaned corpus of the Huggingface Emotion dataset, but you can use your own corpus if you desire.)

Here is an example of how the code is run, and its corresponding output:
![image](https://github.com/SaadHaiderGit/411NLP_Emotion_Sentiment_Predictor/assets/118562950/a8d336f7-0c0e-4942-aec8-47213a744cad)


(DL = Decision List, NBC = Naive Bayes Classifier)
