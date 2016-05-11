
#Import external packages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import time
import pickle as pkl
from sklearn.feature_selection import SelectFromModel

#Import local packages
from WordUtility import WordUtility


def parse_responses(all_responses, parser):
    """

    Parameters
    ----------
    responses
    user_response
    parser

    Returns
    -------

    """
    #Parse out the users response and append to the end of the response list
    clean_all = []

    for rr in range(0, len(all_responses)):
        temp = parser.answer_to_wordlist(all_responses[rr][1])
        temp = [t.replace('.', '') for t in temp]
        clean_all.append(" ".join(temp))

    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 token_pattern='\\b\\w+\\b',
                                 max_features=5000)
    data_features = vectorizer.fit_transform(clean_all)
    data_features = data_features.toarray()
    vocab = vectorizer.get_feature_names()
    #print vocab
    return data_features, vocab, clean_all
