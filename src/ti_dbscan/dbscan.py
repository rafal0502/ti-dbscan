import numpy


def DBSCAN(D, eps, MinPts):
    """Clustering dataset 'D' using DBSCAN algorithm.
       This implementation takes a dataset 'D' (a list
       of vectors), a threshold distance 'eps', and req-
       uired number of points 'MinPts'.

       It returning label -1 (noise), cluster is numbered
       starting from 1
    Args:
        D ([type]): [description]
        eps ([type]): [description]
        MinPts ([type]): [description]
    """

    labels = len(D) * [0]  # initially all labels are 0
    C = 0  # C is the ID of the current cluster

    # Picking new seed points - a point from which
    # to grow a new cluster
    # If valid seed point is found, a new cluster is created
    # and the cluster growth is all handled by the 'expandCluster'
    # rountine

    # For each point P in the dataset D
    # (X - index of datapoint, not datapoint itslef)

    for X in range(0, len(D)):

        # Only points that have not already been claimed
        # can be pciked as new seed points
        # If the point's label is not 0, continue to the next point
        if not (labels[X] == 0):
            continue

        # Find all of X's neighboring points
        NeighborPts = markRegion(D, X, eps)

        # If the number is below MinPts, this point is noise
        # This is the only condition under which a point is labeled
        # NOISE - may be later picked up by another cluster as boundary
        # point (this is only condition under which a cluster label
        # can be changed -- from NOISE to something else)

        if len(NeighborPts) < MinPts:
            labels[X] = -1
        # Otherwise, if there are at lest MinPts nearby,
        # use this point as the seed for a new cluster
        else:
            C += 1
            expandCluster(D, labels, X, NeighborPts, C, eps, MinPts)

        # All data has been clsutered!
    return labels
