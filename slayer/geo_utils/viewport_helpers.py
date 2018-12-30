"""
Functions that make it easier to provide a default centering
for the Viewport, rather than having to toggle parameters
"""


def find_data_centroid(points):
    """Gets centroid in a series of points

    It's worth noting that there's no single
    definition of a multivariate median: http://cgm.cs.mcgill.ca/~athens/Papers/depth.pdf
    """
    avg_x = sum([p[0] for p in points]) / len(points)
    avg_y = sum([p[1] for p in points]) / len(points)
    return (avg_x, avg_y)


def get_bbox(points):
    """Get the bounding box around the data"""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)
    return {
        'top_left': (min_x, max_y),
        'bottom_right': (max_x, min_y)}
