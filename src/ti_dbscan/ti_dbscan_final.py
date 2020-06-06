from typing import List

import numpy


class classDBSCAN:
    def __init__(self, min_points, epsilon):
        self.min_points = min_points
        self.epsilon = epsilon
        self.point_labels = None
        self.cluster_labels = None

    def fit(self, data):
        data = numpy.array(data)

        labels = [0] * len(data)

        cluster_id = 0

        for point in range(0, len(data)):
            # This loop will ensure we get all the clusters

            if labels[point] != 0:
                # Point is already labeled
                continue

            neighbor_points = self.region_query(data, point)

            if len(neighbor_points) < self.min_points:
                # Noise or border point. Cannot expand this point.
                labels[point] = -1
            else:
                # Point is a core point
                cluster_id += 1
                self.grow_cluster(data, labels, point, neighbor_points, cluster_id)

        return labels
