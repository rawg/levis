"""Utilities for working with spatial problems.

Contents:
- **euclidian**: Returns the Euclidian distance between two points.
- **VectorMap**: Maps 2D points to a vector (abstract).
- **NaiveMap**: Implements VectorMap by storing points in a list in the order
  that they were assigned.
- **HilbertMap**: Implements VectorMap by storing the location on a Hilbert
  Curve of the points that are assigned.
- **total_edge_length**: Calculate the total length of internal edges in a
  graph of points. Useful for calculating an attractive score in seating chart
  applications.
- **length_to_nearest**: Calculate the total length from each member of one
  graph to its nearest member in another. Useful for calculating a repulsive
  score in seating chart applications.
"""
from builtins import object

import math

from . import hilbert

def euclidian(x1, y1, x2=None, y2=None):
    """Return the Euclidian distance between two points."""
    if x2 is None and y2 is None:
        if len(x1) is 2 and len(y1) is 2:
            x2, y2 = y1
            x1, y1 = x1
        else:
            raise Exception("Not enough points given.")

    return math.hypot(x2 - x1, y2 - y1)


class VectorMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = []

    def length():
        """Return the number of points in play in this map."""
        raise NotImplementedError("Please implement this method")

    def add(self, pointOrX, y = None):
        """Add a point to the map."""
        raise NotImplementedError("Please implement this method")

    def point_at(self, pos):
        """Return the 2-tuple point that matches a position in the solution."""
        raise NotImplementedError("Please implement this method")

    def index(self, pointOrX, y=None):
        """Return the index of a 2-tuple point in the vector.

        Raises:
            ValueError: if the point is not found.
        """

        if y is None:
            point = pointOrX
        else:
            point = (pointOrX, y)

        return self.points.index(point)

    def length(self):
        return len(self.points)

    def __str__(self):
        return "%s(%d, %d)" % (self.__name__, self.width, self.height)


class NaiveMap(VectorMap):
    def add(self, pointOrX, y=None):
        """Add a point to the map."""
        if y is None:
            point = pointOrX
        else:
            point = (pointOrX, y)

        self.points.append(point)

    def point_at(self, pos):
        return self.points[pos]


class HilbertMap(VectorMap):
    def __init__(self, width, height):
        super(self.__class__, self).__init__(width, height)
        self.curve = hilbert.HilbertCurve(max(width, height))

    def add(self, pointOrX, y=None):
        """Add a point to the map."""
        if y is None:
            point = pointOrX
        else:
            point = (pointOrX, y)

        point1d = self.curve.to_1d(point)
        self.points.append(point1d)
        self.points.sort()

    def point_at(self, pos):
        point1d = self.points[pos]
        return self.curve.to_2d(point1d)

    def index(self, pointOrX, y=None):
        if y is None:
            point = pointOrX
        else:
            point = (pointOrX, y)

        return super(HilbertMap, self).index(self.curve.to_1d(point))

    def __str__(self):
        return "HilbertMap(%d, %d)" % (self.width, self.height)


def total_edge_length(vertices):
    length = 0.0
    visited = {}

    for vert1 in vertices:
        for vert2 in vertices:
            if vert1 != vert2:
                l, r = vert1, vert2
                if l[0] > r[0] or (l[0] == r[0] and l[1] > r[1]):
                    l, r = r, l

                edge = "%d,%d-%d,%d" % (l[0], l[1], r[0], r[1])

                if edge not in visited:
                    distance = euclidian(vert1, vert2)
                    visited[edge] = distance
                    length += distance

    return length

def length_to_nearest(set1, set2):
    length = 0.0

    for vert1 in set1:
        distances = []
        for vert2 in set2:
            distances.append(euclidian(vert1, vert2))

        length += min(distances)

    return length
