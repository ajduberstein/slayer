"""
Functions that make it easier to provide a default centering
for the Viewport, rather than having to toggle parameters
"""
import numpy as np
from scipy.spatial.distance import cdist, euclidean


def geometric_median(X, eps=1e-5):
    """Computes the geometric median of points in n-dimensional space

    Note that there's no single
    definition of a multivariate median: http://cgm.cs.mcgill.ca/~athens/Papers/depth.pdf

    Attribution: https://stackoverflow.com/questions/30299267/geometric-median-of-multidimensional-points
    """
    y = np.mean(X, 0)

    while True:
        D = cdist(X, [y])
        nonzeros = (D != 0)[:, 0]
        Dinv = 1 / D[nonzeros]
        Dinvs = np.sum(Dinv)
        W = Dinv / Dinvs
        T = np.sum(W * X[nonzeros], 0)
        num_zeros = len(X) - np.sum(nonzeros)
        if num_zeros == 0:
            y1 = T
        elif num_zeros == len(X):
            return y
        else:
            R = (T - y) * Dinvs
            r = np.linalg.norm(R)
            rinv = 0 if r == 0 else num_zeros/r
            y1 = max(0, 1-rinv)*T + min(1, rinv)*y
        if euclidean(y, y1) < eps:
            return y1

        y = y1


def find_data_centroid(points):
    """Gets centroid in a series of points

    Args:
        points (:obj:`list` of :obj:`list` of :obj:`float`): List of (x, y) coordinates

    Returns:
        tuple: The centroid of a list of points
    """
    avg_x = sum([p[0] for p in points]) / len(points)
    avg_y = sum([p[1] for p in points]) / len(points)
    return (avg_x, avg_y)


def get_bbox(points):
    """Get the bounding box around the data

    Args:
        points (:obj:`list` of :obj:`list` of :obj:`float`): List of (x, y) coordinates

    Returns:
        dict: Dictionary containing the top left and bottom right points of a bounding box
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)
    return {
        'top_left': (min_x, max_y),
        'bottom_right': (max_x, min_y)}


def k_furthest_points(points, center, k):
    """Gets the k farthest points
    Args:
        points (:obj:`list` of :obj:`list` of :obj:`float`): List of (x, y) coordinates
        k (int): Number of points

    Returns:
        list: index of k furthest points

    Todo:
        More efficient version
    """
    pts_with_distance = np.array([(i, euclidean(pt, center)) for i, pt in enumerate(points)])
    sorted_pts = np.argsort(pts_with_distance, axis=1)
    return [x[0] for x in sorted_pts][:k]


def get_n_pct(points, proportion=1):
    """Computes the bounding box of the maximum zoom for the specified list of points

    Args:
        points (:obj:`list` of :obj:`list` of :obj:`float`): List of (x, y) coordinates
        proportion (float): Value between 0 and 1 representing the minimum proportion of data to be captured

    Returns:
        dict: Dictionary containing the top left and bottom right points of a bounding box

    Todo:
        More efficient version
    """
    if proportion == 1:
        return get_bbox(points)
    # Compute the medioid of the data
    medioid = geometric_median(points)
    # Discard the most distant (1 - proportion) points
    n_to_remove = np.ceil((1 - proportion) * len(points))
    indexes_to_remove = k_furthest_points(points, medioid, n_to_remove)
    deep_copy_points = points[:]
    for i in indexes_to_remove:
        del deep_copy_points[i]
    return get_bbox(deep_copy_points)
