# Implementation of TI-DBSCAN algorithm

## Introduction

Clustering is a technique that groups similar objects such that objects
in the same group are more similar to each other than the objects in the
other groups. The group of similar objects is called a **Cluster**

There are 5 popular clustering algorithms that data scientists need to know:
* K-Means Clustering
* Hierarchical Clustering
* Density-Based Spatial Clustering of Applications with Noise (DBSCAN)
* Mean-Shift Clustering
* Expectation-Maximization (EM) Clustering using Guassian Mixture Models (GMM)



### Description

Proposition of using triangle inequality
property (TI) to reduce the number of
candidates for being a member of Eps-neighboorhood
of a given point.

Major challenges in DBSCAN
* efficient calculation of eps-neightborhood for each of points
* dbscan uses the R*-tree index
* the use of such indices helps in the case of low dimensional data only

### Overview:

DBSCAN refers to unsupervised learning methods that
identify distinctive groups/cluster in data, based
on the idea that a cluster in data space is a contiguous
region of high point density, separated from other such
clusters by continguous regions of low point density.
Density-Based Spatial Clustering of Applications with Noise
can discover clusters of different shapes and sizes from
a large amount of data, which containing noise and outliers.

#### The DBSCAN algorithm uses two parameters:
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


#### Types of points after the DBSCAN clustering is complete:
* core - point that has at least m points within distance n from itself
* border - point that has at least one core point at a distance n
* noise - point that is neither a core nor a border.
          It has less than m points within distance n from itself.


#### Algoritmic steps for DBSCAN clustering:
* the algorithm proceeds by arbitrarily picking up a point
  in the dataset (until all points have been visited)
* if there are at least 'minPoint' points within a radius
  of eps to the point then we consider all these points to
  be part of the same cluster
* the clusters are then expended by recursively repeating
  the neighborhood calculation for each neighboring point




























####   Notes

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

### Disadvantages of DBSCAN

DBSCAN may not be able to discover clusters of different density
The most time-consuming
operation in DBSCAN is the calculation of a neighborhood for each data point. In
order to speed up this operation in DBSCAN, it is expected to be supported by spatial
access methods such as R*-tree. DBSCAN, nevertheless, is not able to
cluster high dimensional data efficiently.

##### Using the Triangle Inequality for Efficient Determination of Eps-Neighborhood
```
For any three points p, q, r:

distance(p,r) <= distance(p,q) + distance(q,r)

More suitable form:

distance(p,q) >= distance(p,r) - distance(q,r)

Let D be a set of points. For any two points p, q in D and any point r:

distance(p,r) - distance(q,r) > Eps  => q ne N(p) & p ne N(q) 

```
###### Notation
```
* D – the set of points that is subject to clustering;
* Eps – the radius of the point neighborhood;
* MinPts – the required minimal number of points MinPts within Eps-neighborhood;
* r – a reference point assumed to be fixed, e.g. to the point with all coordinates equal to 0 or
minimal values in the domains of all coordinates;
* fields of any point p in D:
  - p.ClusterId – label of a cluster to which p belongs; initially assigned the
                  UNCLASSIFIED label;
  - p.dist – the distance of point p to reference point r;-
  - p.NeighborsNo – the number of neighbors of p already found; initially assigned 1 to
                    indicate that a point itself belongs to its own Eps-neighborhood;
  - Border – the information about neighbors of p that turned out non-core points for
             which it is not clear temporary if they are noise ones or border ones; initially assigned
             an empty set;
* D_prim – the result of clustering of D (initially an empty set); 
``` 




###### User’s manual (how to start/run the project)
* Environemnt preparation
```
working dir: ti-dbscan/src/ti_dbscan
conda create -n tidbscan_env
pip install -r requirements.txt
```
* Running sklearn dbscan implementation, my personal implementation of dbscan and tidbscan with exectution time
```
python demo.py
```



#### Sources

[clustering density ~ jing](https://cse.buffalo.edu/~jing/cse601/fa13/materials/clustering_density.pdf)


[Scikit-learn: Machine Learning in Python](https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py)


[Foundations of Intelligent Systems: 19th International Symposium, ISMIS 2011, Warsaw, Poland, June 28-30, 2011, Proceedings](https://books.google.pl/books?id=RfuqCAAAQBAJ&pg=PA289&lpg=PA289&dq=triangle+dbscan+algorithm&source=bl&ots=-MQS78mWrM&sig=ACfU3U0OdjPI1wic9_opoa9mjmOhCySRww&hl=en&sa=X&ved=2ahUKEwiH8p2IvtzpAhXByKQKHWZHDyo4ChDoATACegQIChAB#v=onepage&q=triangle%20dbscan%20algorithm&f=false)

[Kryszkiewicz M., Lasek P. (2010) TI-DBSCAN: Clustering with DBSCAN by Means of the Triangle Inequality. In: Szczuka M., Kryszkiewicz M., Ramanna S., Jensen R., Hu Q. (eds) Rough Sets and Current Trends in Computing, Proceceedings of the 7th International Conference](https://books.google.pl/books?id=vbSqCAAAQBAJ&pg=PA69&lpg=PA69&dq=Kryszkiewicz,+M.;+Lasek,+P.+TI-DBSCAN:+Clustering+with+DBSCAN+by+Means+of+the+Triangle+Inequality.+In+Rough+Sets+and+Current+Trends+in+Computing,+Proceedings+of+the+7th+International+Conference&source=bl&ots=SboA8Vqunc&sig=ACfU3U3mfNAe_J7ccPNZHiIaBEksZlW8Kg&hl=en&sa=X&ved=2ahUKEwif4ID3nuHpAhWKCOwKHXSMBwIQ6AEwAnoECAoQAQ#v=onepage&q=Kryszkiewicz%2C%20M.%3B%20Lasek%2C%20P.%20TI-DBSCAN%3A%20Clustering%20with%20DBSCAN%20by%20Means%20of%20the%20Triangle%20Inequality.%20In%20Rough%20Sets%20and%20Current%20Trends%20in%20Computing%2C%20Proceedings%20of%20the%207th%20International%20Conference&f=false)

[TI-DBSCAN: Clustering with DBSCAN by means of the triangle inequality, In: Szczuka M., Kryszkiewicz M., Ramanna S., Jensen R., Hu Q. (eds) Rough Sets and Current Trends in Computing. RSCTC 2010](https://primo-48tuw.hosted.exlibrisgroup.com/permalink/f/1um23a9/TN_scopus2-s2.0-79956257766)


Kryszkiewicz M., Lasek P. (2010) A Neighborhood-Based Clustering by Means of the Triangle
Inequality. In: Fyfe C., Tino P., Charles D., Garcia-Osorio C., Yin H. (eds) Intelligent Data
Engineering and Automated Learning – IDEAL 2010. IDEAL 2010


