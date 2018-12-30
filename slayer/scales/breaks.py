import numpy as np


def calculate_percentile_breaks(data, num_classes=5):
    """Calculates the percentile cutoff lower bounds for a vector

    Each class will span the same number of units

    Args:
        data (`list` of `float`): Array of data
        num_classes (`int`): Number of desired classes in the data

    Returns:
        (`list of `float`): Sorted quantile values
    """
    return [np.percentile(data, 100 * (x / num_classes)) for x in range(0, num_classes)]


def calculate_equal_interval_breaks(data, num_classes=5):
    """Calculates classes in even intervals across a vector of data

    Each class will have the same number of elements

    Args:
        data (`list` of `float`): Array of data
        num_classes (`int`): Number of desired classes in the data

    Returns:
        (`list` of `float`): Sorted quantile value lists
    """
    max_val, min_val = max(data), min(data)
    increment = (max_val - min_val) / num_classes
    return [min_val + increment * i for i in range(0, num_classes)]


def calculate_jenks_breaks(data, num_classes=5):
    """Calculates "natural" classes across data.

    The variance within each class is minimal while the variance between classes is maximal.

    Not yet implemented.


    Args:
        data (`list` of `float`): Array of data
        num_classes (`int`): Number of desired classes in the data

    Returns:
        (`list` of `float`): Sorted quantile value lists
    """
    raise NotImplementedError()
