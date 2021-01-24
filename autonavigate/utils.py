from cmath import polar
from math import radians, degrees, cos, sin
from typing import Tuple
import sympy
import numpy as np

REGULAR_SAMPLE_STEP = 5  # TODO: sort of magic number here, gotta change in the future


def cart2pol(x: float, y: float) -> Tuple[float, float]:
    r, phi = polar(complex(x, y))
    return r, phi


def pol2cart(r: float, phi: float) -> Tuple[float, float]:
    x = r * cos(phi)
    y = r * sin(phi)
    return x, y


def radians2degrees(r: float) -> float:
    return degrees(r)


def degrees2radians(d: float) -> float:
    return radians(d)


def polygon2axis_parallel_bbox(p: sympy.Polygon) -> Tuple[float, float, float, float]:
    all_x = [pt.x for pt in p.vertices]
    all_y = [pt.y for pt in p.vertices]
    x_min, x_max, y_min, y_max = min(all_x), max(all_x), min(all_y), max(all_y)
    return x_min, x_max, y_min, y_max


def regularly_sampled_coords_in_polygon(p: sympy.Polygon) -> Tuple[sympy.Point2D, ...]:
    # Find the bounding box around the polygon
    x_min, x_max, y_min, y_max = polygon2axis_parallel_bbox(p)
    # Create a regularly sampled grid of points within the polygon
    X, Y = np.meshgrid(
        np.arange(x_min, x_max + REGULAR_SAMPLE_STEP, step=REGULAR_SAMPLE_STEP),
        np.arange(y_min, y_max + REGULAR_SAMPLE_STEP, step=REGULAR_SAMPLE_STEP),
    )
    # Only return the points that fall winside the Polygon
    coords = tuple(
        [
            sympy.Point2D(x, y)
            for x, y in zip(X.flatten(), Y.flatten())
            if p.encloses_point(sympy.Point2D(x, y))
        ]
    )
    return coords


def swap_tuple2(t):
    return t[1], t[0]
