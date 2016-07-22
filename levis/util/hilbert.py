"""
Utilities to map between a 1D Hilbert curve and 2D Euclidian space.

See also:
- https://en.wikipedia.org/wiki/Hilbert_curve
- https://people.sc.fsu.edu/~jburkardt/py_src/hilbert_curve/hilbert_curve.html
- https://en.wikipedia.org/wiki/Moore_curve
"""
from __future__ import division
#from builtins import object

import math

def rotate(s, x, y, rx, ry):
    """Rotate a point."""
    if ry is 0:
        if rx is 1:
            x = s - 1 - x
            y = s - 1 - y

        x, y = y, x
    return (x, y)


def next_power_of_2(i):
    """Get the next power of 2 after ``i``."""
    return int(math.pow(2, math.floor(math.log(i, 2)) + 1))


class HilbertCurve(object):
    """Translates two dimensional points to a Hilbert curve and back."""

    def __init__(self, width):
        if width <= 0:
            raise ValueError("Width must be a positive integer")

        if width & (width - 1) != 0:
            width = next_power_of_2(width)

        self.width = width
        self.length = width ** 2 - 1

    def to_1d(self, pointOrX, y=None):
        """Convert a 2D point to a location on a Hilbert Curve.

        Returns:
            Int: the location along a Hilbert Curve that matches the point.
        """
        if y is None:
            x, y = pointOrX
        else:
            x = pointOrX

        rx = ry = d = 0
        s = old_div(self.width, 2)
        while s > 0:
            rx = int((x & s) > 0)
            ry = int((y & s) > 0)
            d = d + s * s * ((3 * rx) ^ ry)
            x, y = rotate(s, x, y, rx, ry)
            s = int(old_div(s, 2))

        return d

    def to_2d(self, d):
        """Convert a 1D location along a Hilbert Curve to a 2D point.

        Args:
            d (Int): The location along a Hilbert Curve

        Returns:
            (Int, Int): The corresponding 2D point in Euclidian space.
        """
        t = d
        x = y = 0
        s = 1
        while s < self.width:
            rx = (old_div(t, 2)) % 2
            if rx is 0:
                ry = t % 2
            else:
                ry = (t ^ rx) % 2

            x, y = rotate(s, x, y, rx, ry)
            x = x + s * rx
            y = y + s * ry
            t = t / 4
            s = s * 2

        return (x, y)
