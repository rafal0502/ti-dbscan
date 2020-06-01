import numpy


def DBSCAN(D, eps, MinPts):
    """
       Clustering dataset 'D' using DBSCAN algorithm.
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


def expandCluster(D, labels, X, NeighborPts, C, eps, MinPts):
    """
       Expanding cluster beased on seed point X with label C

       This function searches through the dataset to find all 
       points that belong to this new cluster. When this function
       returns, cluster 'C' is complete

    Args:
        D ([type]): List of vectors
                    labels ([type]): List storing the cluster labels 
                    for all dataset points
        X ([type]): Index of the seed point for new cluster
                    NeighborPts ([type]): All of the neighbors of 'X'
        C ([type]): Label for new cluster
                    eps ([type]): Threshold distance
                    MinPts ([type]): Minimum required number of neighbors
    """

    # Assign the cluster lable to the seed point
    labels[X] = C

    # Look at each neighbor of X (Xn - group of n neighbors)
    # NeighborPts will be used as a FIFO queue of points to
    # search - that is, it will grow as we discover new branch
    # points for the cluster. FIFO bahavior - accomplished by
    # using while-loop instead of for-loop
    # In NeighborPts, the points are represented by their index
    # in the original dataset
    i = 0
    while i < len(NeighborPts):

        # get next point from the queue
        Xn = NeighborPts[i]

        # If Xn was labelled NOISE during the seed search,
        # then we know it's not a branch point (it doesn't have
        # enough neighbors), so make it a leaf point of cluster C
        # and move on
        if labels[Xn] == -1:
            labels[Xn] = C

        # Otherwise, if Xn is not already claimed, claim is a part of C
        elif labels[Xn] == 0:
            # Add Xn to cluster C (Assign cluster label C)
            labels[Xn] = C

            # Find all the neighbors of Xn
            XnNeighborsPts = markRegion(D, Xn, eps)

            # If Xn has at least MinPts neighbors, it's a branch point
            # Add all of its neighbors to the FIFO queue to be searched

            if len(XnNeighborsPts) >= MinPts:
                NeighborPts = NeighborPts + XnNeighborsPts

            # If Xn doesn't have enough neighbors, then it's a leaf point
            # Don't queue up it's neighbors as expansion points

        # Advance to the next point in the FIFO queue
        i += 1

    # Growing of cluster C ended


def markRegion(D, X, eps):
    """
       Find all points in dataset 'D' within distance 'eps' of point 'X'
       
       This function calculates the distance between a point X and every
       other point in the dataset, and then returns only those points,
       which are within threshold distance 'eps'.
    Args:
        D ([type]): List of vectors
        X ([type]): Index of the seed point for new cluster
                    NeighborPts ([type]): All of the neighbors of 'X'
        eps ([type]): [description]
    """
    neighbors = []

    # For each point in the dataset...
    for Xn in range(0, len(D)):

        # If the distance is below the threshold, add it to the neighbors list
        if numpy.linalg.norm(D[X] - D[Xn]) < eps:
            neighbors.append(Xn)

    return neighbors
