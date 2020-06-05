# Ploting results
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from classdbscan import classDBSCAN
from dbscan import basicDBSCAN
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import time

# Create three gaussian blobs to use as our clustering data.
# First tests on dummy data

centers = [[1, 1], [-1, -1], [1, -1]]

X, labels_true = make_blobs(
    n_samples=750, centers=centers, cluster_std=0.4, random_state=0
)


X = StandardScaler().fit_transform(X)

# Scikit-learn implementation of DBSCAN
#
print("Runing scikit-learn implementation...")
start_time = time.clock()
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
print(f"Execution scikit-learn implementation: {time.clock() - start_time} seconds")
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
basic_labels = basicDBSCAN(X, eps=0.3, MinPts=10)
basic_core_samples_mask = np.zeros_like(basic_labels, dtype=bool)


# Number of clusters in labels, ignoring noise if present.
basic_n_clusters_ = len(set(basic_labels)) - (1 if -1 in basic_labels else 0)
basic_n_noise_ = list(basic_labels).count(-1)

print("basicDBSCAN part of visualization...")


# Black removed and is used for noise instead
unique_basic_labels = set(basic_labels)

fig = plt.figure(figsize=(10, 10))
sns.scatterplot(X[:, 0], X[:, 1], hue=["cluster-{}".format(x) for x in basic_labels])
plt.title(f"Estimated number of basicDBSCAN clusters: {basic_n_clusters_}")
plt.show()

# Run my CLASSDBSCAN implementation.
print("Runing classDBSCAN implementation...")
classdb = classDBSCAN(min_points=10, epsilon=0.3)
class_labels = classdb.fit(X)
class_core_samples_mask = np.zeros_like(class_labels, dtype=bool)


# Number of clusters in labels, ignoring noise if present.
class_n_clusters_ = len(set(class_labels)) - (1 if -1 in class_labels else 0)
class_n_noise_ = list(class_labels).count(-1)


print("classDBSCAN part of visualization...")


# Black removed and is used for noise instead
unique_class_labels = set(class_labels)

fig = plt.figure(figsize=(10, 10))
sns.scatterplot(X[:, 0], X[:, 1], hue=["cluster-{}".format(x) for x in class_labels])
plt.title(f"Estimated number of clusters by classDBSCAN: {class_n_clusters_}")
plt.show()


###############################################################################
# Checking we get the same results?

num_disagree = 0

# Go through each label and make sure they match (print the labels if they
# don't)
for i in range(0, len(sklearn_labels)):
    if not sklearn_labels[i] == basic_labels[i]:
        print(f"Scikit learn: {sklearn_labels[i]} mine: {basic_labels[i]}")
        num_disagree += 1

if num_disagree == 0:
    print("All labels match!")
else:
    print(f"Fail, {num_disagree} labels don't match.")
