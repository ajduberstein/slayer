from __future__ import absolute_import

from collections import OrderedDict
from warnings import warn

import pandas as pd

from .scales.colors import DEFAULT_PALETTES, get_random_rgb
from .scales.breaks import calculate_breaks, VALID_SCALES
from .scales.interpolate import interpolate


class ColorScale(object):
    """Computes a lookup between a vector of data and color values across
    the data.

    Inspired by the way QGIS handles colors.

    Args:
        variable_name (str):
        palette (:obj:`str` or :obj:`list` of :obj:`list`):
    """

    def __init__(
        self,
        palette=None,
        variable_name=None,
        reverse_colors=False,
        scale_type='quantile',
        num_classes=5,
        display_formatter=None,
        data=None
    ):
        # Set palette
        if isinstance(palette, str) and palette in DEFAULT_PALETTES.keys():
            self.palette = DEFAULT_PALETTES[palette]
        elif isinstance(palette, list):
            self.palette = palette
        else:
            raise Exception('`palette` must be a `list` of RGB values or a `str` indicating one of a list '
                            'of common ColorBrewer palettes: %s' % ', '.join(DEFAULT_PALETTES.keys()))
        if reverse_colors is True:
            self.palette = palette[::-1]

        if not isinstance(variable_name, str):
            raise Exception('`variable_name` must be a string represented in the data set headers.')
        self.variable_name = variable_name

        if scale_type not in VALID_SCALES:
            raise Exception('`scale_type` must be one of the following: %s' % ', '.join(VALID_SCALES))
        self.scale_type = scale_type
        self.num_classes = num_classes
        if data is not None:
            self.set_data(data)
        self.display_formatter = display_formatter

    def set_data(self, data):
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            self.data_vector = [d[self.variable_name] for d in data]
        elif isinstance(data, pd.DataFrame):
            self.data_vector = data[self.variable_name]
        else:
            raise TypeError('Data can only be set from a pandas.DataFrame, received', type(data))

        if self.scale_type in ('categorical', 'categorical_random'):
            self.breaks = produce_categorical_gradient(self.data_vector, self.scale_type, self.palette)
            self.gradient_lookup = produce_categorical_gradient(self.data_vector, self.scale_type, self.palette)
        else:
            breaks = calculate_breaks(self.data_vector, self.scale_type, self.num_classes)
            self.gradient_lookup = produce_numerical_gradient(breaks, self.palette)

    def get_gradient_lookup(self, for_display=False):
        if self.gradient_lookup is None:
            raise ValueError('Data must be set to get the gradient lookup')
        if for_display:
            display_dict = OrderedDict([])
            for k in self.gradient_lookup.keys():
                str_rgba = ', '.join([str(int(x)) for x in self.gradient_lookup[k]])
                display_k = self.display_formatter % k if self.display_formatter else k
                display_dict[display_k] = str_rgba
            return display_dict
        return self.gradient_lookup

    def is_categorical(self):
        """Returns True if categorical scale, False otherwise"""
        return self.scale_type in ('categorical', 'categorical_random')


def produce_categorical_gradient(data_vector, scale_type, palette):
    # Choose from a common gradient
    classes = sorted(list(set(data_vector)))
    if scale_type == 'categorical' and len(classes) > len(palette):
        warn('Number of categories for the specified column is greater '
             'than the number of colors available in the color palette. '
             'The legend will contain duplicate colors.')
    colors = []
    for i, c in enumerate(classes):
        if scale_type == 'categorical':
            colors.append(palette[i % len(palette)])
        elif scale_type == 'categorical_random':
            colors.append(get_random_rgb())
    return OrderedDict([item for item in zip(classes, colors)])


def produce_numerical_gradient(breaks, palette):
    gradient = []
    num_breaks = len(breaks)
    for i, lower_bound in enumerate(breaks):
        break_percentage = float(i) / num_breaks
        gradient.append(interpolate(palette, break_percentage))
    return OrderedDict(zip(breaks, gradient))
