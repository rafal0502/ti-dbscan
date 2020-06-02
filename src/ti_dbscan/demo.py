# Ploting results
import matplotlib.pyplot as plt
import numpy as np
from dbscan import basicDBSCAN
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

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
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
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
print(
    f"Sklearn number of cluster: {sklearn_n_clusters_}, number of noises: {sklearn_n_noise_}"
)


# My implementation of DBSCAN
#
# Run my DBSCAN implementation.
print("Running my implementation...")
my_labels = basicDBSCAN(X, eps=0.3, MinPts=10)
my_core_samples_mask = np.zeros_like(my_labels, dtype=bool)
# print(my_labels)

# Number of clusters in labels, ignoring noise if present.
my_n_clusters_ = len(set(my_labels)) - (1 if -1 in my_labels else 0)
my_n_noise_ = list(my_labels).count(-1)
print(f"My number of cluster: {my_n_clusters_}, number of noises: {my_n_noise_}")

###############################################################################
# Checking we get the same results?

num_disagree = 0

# Go through each label and make sure they match (print the labels if they
# don't)
for i in range(0, len(sklearn_labels)):
    if not sklearn_labels[i] == my_labels[i]:
        print(f"Scikit learn: {sklearn_labels[i]} mine: {my_labels[i]}")
        num_disagree += 1

if num_disagree == 0:
    print("All labels match!")
else:
    print(f"Fail, {num_disagree} labels don't match.")


print("Sklearn part of visualization...")


unique_sklearn_labels = set(sklearn_labels)
print(f"List of unique sklearn lables {unique_sklearn_labels}")


# Black removed and is used for noise instead.
unique_sklearn_labels = set(sklearn_labels)
colors = [
    plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_sklearn_labels))
]

print(f"Sklearn colors {colors}")
for k, col in zip(unique_sklearn_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]
    sklearn_class_member_mask = sklearn_labels == k

    xy = X[sklearn_class_member_mask & sklearn_core_samples_mask]
    print(f"Before sklearn plot {xy}")
    plt.plot(
        xy[:, 0],
        xy[:, 1],
        "o",
        markerfacecolor=tuple(col),
        markeredgecolor="k",
        markersize=14,
    )

    xy = X[sklearn_class_member_mask & ~sklearn_core_samples_mask]
    print(f"Before sklearn plot {xy}")
    plt.plot(
        xy[:, 0],
        xy[:, 1],
        "o",
        markerfacecolor=tuple(col),
        markeredgecolor="k",
        markersize=6,
    )

plt.title(f"Estimated number of sklearn clusters {sklearn_n_clusters_}")
plt.show()


print("basicDBSCAN part of visualization...")


# Black removed and is used for noise instead
unique_my_labels = set(my_labels)
print(f"List of unique my lables {unique_my_labels}")


my_colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_my_labels))]

for k, col in zip(unique_sklearn_labels, my_colors):
    if k == -1:
        col = [0, 0, 0, 1]

    my_class_member_mask = my_labels == k
    xy = X[my_class_member_mask & my_core_samples_mask]
    print(f"Before my plot {xy}")

    plt.plot(
        xy[:, 0],
        xy[:, 1],
        "o",
        markerfacecolor=tuple(col),
        markeredgecolor="k",
        markersize=14,
    )

    xy = X[my_class_member_mask & ~my_core_samples_mask]
    print(f"Before my plot {xy}")
    plt.plot(
        xy[:, 0],
        xy[:, 1],
        "o",
        markerfacecolor=tuple(col),
        markeredgecolor="k",
        markersize=6,
    )

plt.title(f"Estimated number of clusters by basicDBSCAN: {my_n_clusters_}")
plt.show()
