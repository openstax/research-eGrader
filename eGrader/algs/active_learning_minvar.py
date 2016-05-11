# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:38:29 2016

@author: drew
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier


def get_fit_probabilities(features, forest):
    """
    The only reason this function exists is to handle cases where there
    is only one class label (0 or 1) present.

    Parameters
    ----------
    features
    forest

    Returns P
    -------

    """

    P = forest.predict_proba(features)

    if (forest.n_classes_ < 2):
        #Check to see if we only have zero
        if (forest.classes_ == 0):
            P = np.concatenate((P, np.ones((P.shape[0], 1))),
                               axis=1)
        else:
            P = np.concatenate((np.zeros((P.shape[0], 1)), P),
                               axis=1)
    return P


def get_min_var_idx(orig_features,
                    orig_labels,
                    orig_forest,
                    sample_limit=None):
    """

    Parameters
    ----------
    orig_features
    orig_labels
    orig_forest
    sample_limit

    Returns
    -------

    """
    #Grab the observed/unobserved indices
    obs_idx = np.where(~np.isnan(orig_labels))[0]
    unobs_idx_full = np.where(np.isnan(orig_labels))[0]

    #Now handle sample limit -- make sure not larger than sample space
    #Then choose randomly which indices will be considered during this iter
    if (sample_limit is not None):
        sample_limit_min = min(sample_limit,
                               len(unobs_idx_full))
        unobs_idx = np.random.choice(unobs_idx_full,
                                     sample_limit_min,
                                     replace=False)
    else:
        unobs_idx = unobs_idx_full

    #Compute the fit probabilities on the unobserved set
    P = get_fit_probabilities(orig_features[unobs_idx, :],
                              orig_forest)

    #Now loop over the selected unobserved indices
    #For each one, we calculate the expected variance and store this off
    var_v = np.zeros(len(unobs_idx))
    for uu in range(0, len(unobs_idx)):

        #Copy these so we don't screw stuff up . . .
        labels = np.copy(orig_labels)
        features = np.copy(orig_features)

        selection_idx = unobs_idx[uu]
        train_idx = np.append(obs_idx, selection_idx)
        forest = RandomForestClassifier(n_estimators=10)

        #Do the case where label is 0
        labels[selection_idx] = 0
        forest = train_random_forest(features[train_idx, :],
                                     labels[train_idx])
        P0 = get_fit_probabilities(features[unobs_idx, :],
                                   forest)

        var_0 = np.sum(P0[:, 0] * P0[:, 1])

        #Do the case where label is 0
        labels[selection_idx] = 1
        forest = train_random_forest(features[train_idx, :],
                                     labels[train_idx])
        P1 = get_fit_probabilities(features[unobs_idx, :],
                                   forest)

        var_1 = np.sum(P1[:, 0] * P1[:, 1])

        # Compute the expectated variance
        var_v[uu] = P[uu, 0] * var_0 + P[uu, 1] * var_1

    # Now make the final selection
    v_min = np.argmin(var_v)
    return unobs_idx[v_min]


def train_random_forest(features, labels, num_trees=10):
    """

    Parameters
    ----------
    features
    labels
    num_trees

    Returns
    -------

    """
    forest = RandomForestClassifier(n_estimators=num_trees)
    forest = forest.fit(features,
                        labels)
    return forest


def update_classifiers_minimum_variance(features,
                                        labels,
                                        ground_truth_labels,
                                        current_forest=None,
                                        sample_limit=None):
    """
    Parameters
    ----------
    features : array
        A numpy array of features with R x V dimensions, where R is the number of responses and V is the vocabulatry
    labels: array
        Labels length should be equivalent to features X-axis ex. features.shape[0]. This represents the observed vs
        unobserved responses.
    ground_truth_labels: array
        The labels that are provided by the grader junk/not-junk
    current_forest: forest or None
        This is provided if needing to re-train the forest classifier
    sample_limit : int or None
        maximum number of samples to train for the classifier

    Returns
    -------
    forest : forest classifier
        forest classifier

    Notes
    -----


    """
    # Check to see if there is any labeled data -- if not just pick one
    if np.all(np.isnan(labels)):
        selection_idx = np.random.choice(len(labels))
        labels[selection_idx] = ground_truth_labels[selection_idx]
        forest = train_random_forest(features[selection_idx, :],
                                     labels[selection_idx, :])
        return forest

    # Grab the observed/unobserved indices
    obs_idx = np.where(~np.isnan(labels))[0]

    # Check to see if there is no current classifier -- if not then make
    if current_forest is None:
        current_forest = train_random_forest(features[obs_idx, :],
                                             labels[obs_idx])

    # Now, find the entry that will minimize expected variance
    selection_idx = get_min_var_idx(features,
                                    labels,
                                    current_forest,
                                    sample_limit)

    labels[selection_idx] = ground_truth_labels[selection_idx]
    train_idx = np.append(obs_idx, selection_idx)

    # Retrain the forest with the updated observation set
    forest = train_random_forest(features[train_idx, :],
                                 labels[train_idx, :])
    return forest
