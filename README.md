# Implementation of TI-DBSCAN algorithm


## Description

Proposition of using triangle inequality
property (TI) to reduce the number of
candidates for being a member of Eps-neighboorhood
of a given point.

Major challenges in DBSCAN
* efficient calculation of eps-neightborhood for each of points
* dbscan uses the R*-tree index
* the use of such indices helps in the case of low dimensional data only


## Overview:

DBSCAN refers to unsupervised learning methods that
identify distinctive groups/cluster in data, based
on the idea that a cluster in data space is a contiguous
region of high point density, separated from other such
clusters by continguous regions of low point density.
Density-Based Spatial Clustering of Applications with Noise
can discover clusters of different shapes and sizes from
a large amount of data, which containing noise and outliers.

## The DBSCAN algorithm uses two parameters:
* eps:  a distance measure that is used to locate the points
        in the neighborhood of any point
* minPts: minimum number of points (threshold) clustered
        together for a region to be considered dense

It's much easier to understand these parameters if we
explore two concept called Density Connectivity and Reachability

* reachability - in terms of density establishes a point
                 to be reachable fro another if it lies within a
                 particular distance (eps) from it

* connectivity - involves a transitivity based chaining-approach
                 to determine wheter points are located in a par-
                 ticular cluster


## Types of points after the DBSCAN clustering is complete:
* core - point that has at least m points within distance n from itself
* border - point that has at least one core point at a distance n
* noise - point that is neither a core nor a border.
          It has less than m points within distance n from itself.


## Algoritmic steps for DBSCAN clustering:
* the algorithm proceeds by arbitrarily picking up a point
  in the dataset (until all points have been visited)
* if there are at least 'minPoint' points within a radius
  of eps to the point then we consider all these points to
  be part of the same cluster
* the clusters are then expended by recursively repeating
  the neighborhood calculation for each neighboring point




























## Notes

Clustering analysis is an unsupervised learning method that
separates the data points into several specific bunches of
groups, souch that the data points in the same group have
similar properties and points in different groups have different
properties in some sens.

Summing up, all clustering methods use the same approach i.e.
first we calculate similarities and then we use it to cluster
the data points into groups or batches.


#### Density-Based clustering algorithm (DBSCAN) vs K-means clustering

![DbscanvsKmeans](dbclustering-kmeans.png)


K-means clustering may cluster loosely related observations together,
even if the observations are scattered far away in the space.
Each data point plays a role in forming the cluster (because clusters
depend on the mean value of cluster elements). So, slight change in
data points might affect the clustering outcome. Due to the way clus-
ters are formed by DBSCAN this problem is greatly reduced. It's not
a problem at all, unless we come across some odd shape data.

Another plus of DBSCAN is that you don't need to specify the number
of clusters ("k") in order to use it as in k-means method. All you
need is a function to calculate the distance between values and some
guidance for what amount of distance is considered "close". Thanks to
that, DBSCAN produces more reasonable results that k-means across a
variety of different distributions. Image below:


#### For simplified process of implementation I started from pseudocode and basic version of DBSCAN

```
DBSCAN(D, eps, MinPts)
 C = 0
 for each unvisited point P in dataset D
  mark P as visited
  NeighborPts = regionQuery(P, eps)
  if sizeof(NeighborPts) < MinPts
    mark P as NOISE
  else
    C = next cluster
    expandCluster(P, NeighborPts, C, eps, MinPts)

expandCluster(P, NeighborPts, C, eps, MinPts)
  add P to cluster C
  for each point P' in NeighborPts
    if P' is not visited
      mark P' as visited
      NeighborPts' = regionQuery(P',eps)
      if sizeof(NeighborPts') >= MinPts
        NeighborPts = NeighborPts joined with NeighborPts'
    if P' is not yet member of any cluster
      add P' to cluster C

regionQuery(P, eps)
  return all points within P's eps-neighborhood(including P)
```
### Sources

[clustering density ~ jing](https://cse.buffalo.edu/~jing/cse601/fa13/materials/clustering_density.pdf)


[Scikit-learn: Machine Learning in {P}ython](https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py)
