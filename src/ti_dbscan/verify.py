# Ploting results
import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from dbscan import basicDBSCAN
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from ti_dbscan import TI_DBScan
import pandas as pd





if __name__ == '__main__':
    df = pd.read_csv("iris.csv", header=None,usecols=[0,3])
    X = df.values
    print("Runing scikit-learn implementation...")
    scikit_start_time = time.monotonic()
    db = DBSCAN(eps= 0.3, min_samples=10).fit(X)  #eps 0.3 min_samples 10
    scikit_end_time = time.monotonic()
    scikit_learn_time = scikit_end_time - scikit_start_time
    print(f"Execution scikit-learn implementation: {scikit_learn_time} seconds")
    sklearn_core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    sklearn_labels = db.labels_

    # Scikit learn uses -1 to for NOISE, and starts cluster labeling at 0.
    # I started numbering at 1, so increment the sklearn cluster numbers by 1.
    for i in range(0, len(sklearn_labels)):
        if not sklearn_labels[i] == -1:
            sklearn_labels[i] += 1


    # Number of clusters in labels, ignoring noise if present.
    sklearn_n_clusters_ = len(set(sklearn_labels)) - (1 if -1 in sklearn_labels else 0)
    sklearn_n_noise_ = list(sklearn_labels).count(-1)

    print("Sklearn part of visualization...")
    unique_sklearn_labels = set(sklearn_labels)

    fig = plt.figure(figsize=(10, 10))
    sns.scatterplot(X[:, 0], X[:, 1], hue=["cluster-{}".format(x) for x in sklearn_labels])
    plt.title(f"Estimated number of sklearn clusters: {sklearn_n_clusters_}")
    plt.show()



    # My implementation of DBSCAN
    #
    # Run my DBSCAN implementation.
    print("Running basicDBSCAN implementation...")
    basic_start_time = time.monotonic()
    basic_labels = basicDBSCAN(X, eps=0.3, MinPts=10)
    basic_end_time = time.monotonic()
    basicDBSCAN_time = basic_end_time - basic_start_time
    print(f"Execution time basicDBSCAN implementation: {basicDBSCAN_time} seconds")
    basic_core_samples_mask = np.zeros_like(basic_labels, dtype=bool)


    # Number of clusters in labels, ignoring noise if present.
    basic_n_clusters_ = len(set(basic_labels)) - (1 if -1 in basic_labels else 0)
    basic_n_noise_ = list(basic_labels).count(-1)

    print("basicDBSCAN part of visualization...")
    unique_basic_labels = set(basic_labels)

    fig = plt.figure(figsize=(10, 10))
    sns.scatterplot(X[:, 0], X[:, 1], hue=["cluster-{}".format(x) for x in basic_labels])
    plt.title(f"Estimated number of basicDBSCAN clusters: {basic_n_clusters_}")
    plt.show()




    # Run my TIDBSCAN implementation.
    print("Running TIDBSCAN implementation...")
    tidbscan_start_time = time.monotonic()
    tidbscan_labels = []
    #tidbscan_labels =TI_DBScan(X, eps=0.3, MinPts=10)
    result =TI_DBScan(X, eps=0.3, MinPts=10)
    tidbscan_end_time = time.monotonic()
    for element in result:
        tidbscan_labels.append(element.ClusterId)   
    #TIDBscan uses -1 to for NOISE, and starts cluster labeling at 0.
    #I started numbering at 1, so increment the tidbscan cluster numbers by 1.
    for i in range(0, len(tidbscan_labels)):
        if not tidbscan_labels[i] == -1:
            tidbscan_labels[i] += 1            
    TIDBSCAN_time = tidbscan_end_time - tidbscan_start_time
    print(f"Execution time TIDBSCAN implementation: {TIDBSCAN_time} seconds")
    tidbscan_core_samples_mask = np.zeros_like(tidbscan_labels, dtype=bool)


    # Number of clusters in labels, ignoring noise if present.
    tidbscan_n_clusters_ = len(set(tidbscan_labels)) - (1 if -1 in tidbscan_labels else 0)
    tidbscan_n_noise_ = list(tidbscan_labels).count(-1)

    print("TIDBSCAN part of visualization...")
    unique_basic_labels = set(tidbscan_labels)

    fig = plt.figure(figsize=(10, 10))
    sns.scatterplot(X[:, 0], X[:, 1], hue=["cluster-{}".format(x) for x in tidbscan_labels])
    plt.title(f"Estimated number of TIDBSCAN clusters: {tidbscan_n_clusters_}")
    plt.show()
