import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import SGDClassifier
import xgboost as xgb
from sklearn.neighbors import KNeighborsClassifier
import pickle


def getTextProbs(text):
    model_filename = 'textClassifer.pkl'
    vectorizer = 'vectorizer.pkl'

    with open(model_filename, 'rb') as model_file:
        loaded_ensemble = pickle.load(model_file)

    new_text_vectorized = vectorizer.transform([text])
    prediction = loaded_ensemble.predict_proba(new_text_vectorized)
    return prediction 