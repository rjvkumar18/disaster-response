"""
This module is responsible for ML pipeline
Loads data from sqlite db, trains & evaluates the ML model 
Saves the trained model as a pickle file
"""

# import required libraries
import sys
import nltk
nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger'])
import re
import pickle
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import GradientBoostingClassifier,AdaBoostClassifier
from sklearn.metrics import make_scorer, accuracy_score, f1_score, fbeta_score, classification_report
from sqlalchemy import create_engine

def load_data(database_filepath):
    """
    Loads the from the database

    Parameters
    ----------
    database_filepath : Path to sqlite db

    Returns
    -------
    X : Feture dataframe
    Y : Label dataframe
    category_names : For data visualisation
    """
    
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql_table('MessageCategory', engine)
    X = df['message'] 
    Y = df.iloc[:,4:]
    category_names = Y.columns
    return X, Y, category_names


def tokenize(text):
    """
    Tokenization function to process the text data

    Parameters
    ----------
    text : List of text messages
    
    Returns
    -------
    clean_tokens : Tokenized text to feed ML model
    """
    
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

class StartingVerbExtractor(BaseEstimator, TransformerMixin):
    """
    This class is responsible for extracting starting verb of a sentence,
    creating new feature for the ML classifier
    """

    def starting_verb(self, text):
        sentence_list = nltk.sent_tokenize(text)
        for sentence in sentence_list:
            pos_tags = nltk.pos_tag(tokenize(sentence))
            first_word, first_tag = pos_tags[0]
            if first_tag in ['VB', 'VBP'] or first_word == 'RT':
                return True
        return False

    def fit(self, x, y=None):
        return self

    def transform(self, X):
        X_tagged = pd.Series(X).apply(self.starting_verb)
        return pd.DataFrame(X_tagged)


def build_model():
    """
    This function returns a scikit-learn ML Pipeline that processs text messages
    according to NLP best practices using feature union and applying a classifier
    """

    model = Pipeline([
        ('features', FeatureUnion([

            ('text_pipeline', Pipeline([
                ('vect', CountVectorizer(tokenizer=tokenize)),
                ('tfidf', TfidfTransformer())
            ])),

            ('starting_verb', StartingVerbExtractor())
        ])),

        ('clf', MultiOutputClassifier(AdaBoostClassifier()))
    ])
    
    return model


def evaluate_model(model, X_test, Y_test, category_names):
    """
    This function applies ML pipeline to the test set and prints out
    model performance
    
    Parameters:
    model : ML Pipeline
    X_test : test feature
    Y_test : test labels
    category_names : label names
    """

    y_pred = model.predict(X_test)
    overall_accuracy = (y_pred == Y_test).mean().mean()
    print('Average overall accuracy {0:.2f}% \n'.format(overall_accuracy*100))

    y_pred_pd = pd.DataFrame(y_pred, columns = Y_test.columns)
    for column in Y_test.columns:
    	print('------------------------------------------------------\n')
    	print('FEATURE: {}\n'.format(column))
    	print(classification_report(Y_test[column],y_pred_pd[column]))
    pass


def save_model(model, model_filepath):
    """
    This function saves the trained model as a pickle file, to be loaded later.
    
    Parameters:
    model : ML Pipelin object
    model_filepath : The path where the .pkl file is saved
    """

    filename = model_filepath
    pickle.dump(model, open(filename, 'wb'))
    pass


def main():
    """
    This function executes the ML Pipeline by,
    Loading data from sqlite db
    Training ML model on training set
    Evaluating model performance on test set
    Saving trained model as a pickle file
    """
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()