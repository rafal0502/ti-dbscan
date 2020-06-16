import numpy as np
import operator


def TI_Forward_Neighborhood(D, p, Eps):
    """ ."""
    seeds = []
    forwardThreshold = p.dist + Eps
    # You have to declare the list to traverse.
    # First is the index with element "p" 
    # Items are selected from start to item "p"
    # And finally it turns around
    indice = D.index(p)
    points_list = D[indice + 1:]

   # The newly calculated list is traversed
    for q in points_list:
        if q.dist > forwardThreshold:
            break
        if Distance(q.Coords, p.Coords) <= Eps:
            seeds.append(q)

    # The list with the seeds is returned.
    return seeds


def TI_Backward_Neighborhood(D, pto, Eps):
    seeds = []
    backwardThreshold = pto.dist - Eps
    # You have to declare the list to go.
    # First is the index where the element "p" is
    # Items are selected from start to item "p"
    # And finally he turns around
    indice = D.index(pto)
    points_list = D[:indice]
    points_list.reverse()

    # The newly calculated list is traversed
    for q in points_list:
        if q.dist < backwardThreshold:
            break
        if Distance(q.Coords, pto.Coords) <= Eps:
            seeds.append(q)
    # The list with the seeds is returned.
    return seeds


def TI_Neighborhood(D, p, Eps):
    part_1 = TI_Backward_Neighborhood(D, p, Eps)
    part_2 = TI_Forward_Neighborhood(D, p, Eps)
    return part_1 + part_2


def TI_ExpandCluster(D, D_prim,
                     p, ClId, Eps, MinPts):
    """D is increasingly ordered with respect to the
    distances from the reference point"""

    # The set of points around point "p" is explored. Note that
    # seeds is a set or list of points.
    seeds = TI_Neighborhood(D, p, Eps)
    # Points around "p" are counted, including itself
    p.NeighborsNo += len(seeds)
    # "p" can be noise or an edge point
    if p.NeighborsNo < MinPts:
        # It is initially declared as noise
        p.ClusterId = -1  # "NOISE"
        # You go through each point of the set of seeds
        for q in seeds:
            q.Border.append(p)
            q.NeighborsNo += 1

        # The list of edge points of "p" is declared empty
        p.Border = []
        # "P" is removed from D to D_prim
        D.remove(p)
        D_prim.append(p)
        return False

    else:
        # Cluster membership is assigned
        p.ClusterId = ClId
        # The points found in the seeds are covered
        for q in seeds:
            q.ClusterId = ClId
            q.NeighborsNo += 1

        for q in p.Border:
            # Identify which element is in the D_prim listing, and
            # then modify this.
            D_prim[D_prim.index(q)].ClusterId = ClId

        # Once again the set is emptied
        p.Border = []
        # "P" is removed from D to D_prim
        D.remove(p)
        D_prim.append(p)
        # As long as the number of elements in the seed list is
        # greater than zero, that is, while finding ONE element, the
        # next iteration:
        while seeds:
            # Somehow in this while the process is repeated
            curPoint = seeds[0]
            curSeeds = TI_Neighborhood(D, curPoint, Eps)
            curPoint.NeighborsNo += len(curSeeds)
            # i curPoint is on the edge
            if curPoint.NeighborsNo < MinPts:
                for q in curSeeds:
                    q.NeighborsNo += 1
            # If curPoint is core
            else:
                while curSeeds:
                    q = curSeeds[0]
                    q.NeighborsNo += 1
                    if q.ClusterId == "UNCLASSIFIED":
                        q.ClusterId = ClId
                        # Remove "p" from D to
                        # D_prim
                        curSeeds.remove(q)
                        seeds.append(q)
                    else:
                        curSeeds.remove(q)
                # The edge points are traversed
                for q in curPoint.Border:
                    # Identify which element is in the
                    # listing D_prim, and then this is modified.
                    D_prim[D_prim.index(q)].ClusterId = ClId           
            # The content of the variables is modified
            curPoint.Border = []
            D.remove(curPoint)
            D_prim.append(curPoint)
            seeds.remove(curPoint)
        # The logical value is returned.
        return True


def Distance(point, pnt_ref):
    """Function that calculates the distance in two dimensions"""
    point = np.array(point[0:2])
    pnt_ref = np.array(pnt_ref[0:2])
    return np.sqrt(np.sum(np.power(point - pnt_ref, 2)))


class class_point:
    """Class that generates a point with its attributes"""
    def __init__(self, point, pnt_ref, metadata=None):
        try:
            # Metadata
            self.metadata = metadata
            # The original coordinates are saved
            self.Coords = point[0:2]
        except:
            pass

        # p.ClusterId = UNCLASSIFIED;
        self.ClusterId = "UNCLASSIFIED"
        # p.dist = Distance(p,r)
        self.dist = Distance(point[0:2], pnt_ref[0:2])
        # p.NeighborsNo = 1
        self.NeighborsNo = 1
        # p.Border = vacio
        self.Border = []


def TI_DBScan(D, eps, MinPts, metadata=None):
    """This class applies the TI-DBScan algorithm to the set
    of points delivered.
    D = [[coord1, coord2, ...], ...]:
        It is a list of tuples or lists, where the two
    first items in each list are the coordinates and
    the third is METAdata."""
    try:
        # /* assert: r denotes a reference point */
        pnt_ref = D[0]
    except IndexError:
        pass
    # the number of points cannot be 1.
    MinPts = MinPts if MinPts > 1 else 2

    # D' = empty set of points;
    D_prim = []
    #Points are transformed
    try:
        D = [class_point(
            D[indice], pnt_ref, metadata=metadata[indice])
            for indice in range(len(D))]
    except TypeError:
        D = [class_point(
            D[indice], pnt_ref)
            for indice in range(len(D))]

        # sort all points in D non-decreasingly w.r.t. field dist;
        #D = sorted(D, key=operator.attrgetter('dist'))
    D = sorted(D, key=operator.attrgetter('dist'))

    # ClusterId = label of first cluster;
    i = 0
    ClusterId = i #"%s" % (

    # for each point p in the ordered set D starting from
    # the first point until last point in D do
    # While the list of points to review is not empty, it iterates
    # infinitely.
    while D:
        p = D[0]
        #for p in D:
        # if TI-ExpandCluster(D, D', p, ClusterId, Eps, MinPts) then
        if TI_ExpandCluster(D, D_prim,
                            p, ClusterId, eps, MinPts):
            # ClusterId = NextId(ClusterId)
            i += 1
            ClusterId = i #"%s" % (i)
            # endif
        # endfor

    # return D'// D' is a clustered set of points
    return D_prim


# The next line is for testing
if __name__ == "__main__":
    set_of_points = [[1.00, 1.00], [1.50, 1.00], [2.00, 1.50],
                          [5.00, 5.00], [6.00, 5.50], [5.50, 6.00],
                          [10.00, 11.00], [10.50, 9.50], [10.00, 10.00],
                          [8.00, 1.00], [1.00, 8.00]]

    #set_of_points = [[1.00, 1.00], [1.50, 1.00], [2.00, 1.50],
     #                    [5.00, 5.00], [6.00, 5.50], [5.50, 6.00],
      #                   [8.00, 1.00], [1.00, 8.00]]

    #set_of_points = [[1.00, 1.00], [1.50, 1.00], [2.00, 1.50],
     #                     [5.00, 5.00], [8.00, 1.00], [1.00, 8.00]]

    result = TI_DBScan(set_of_points, 2, 2)

    for element in result:
        print (element.ClusterId)
        print (element.Coords)
        print ("")