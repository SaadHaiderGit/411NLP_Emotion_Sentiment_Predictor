# Emotion Sentiment Predictor

This is the source code for a emotion sentiment predictor. It uses a corpus gained from the Huggingface Emotion dataset, and can determine six different emotions: joy, sadness, anger, fear, surprise, and love.

The code uses no NLP or machine learning libraries and instead has a model made from scratch for this specific task, using a Naive Bayes Classifier system. The data is also divided into five folds, with four for training and one for testing; the model has five rounds where a new fold is used for testing (and the rest for training), until all folds have been used. The average accuracy is calculated this way.

The provided code does little other than showing accuracy results, but it may be in one's interest to run it to see it working. You can take the github link and clone it to your local repo.
