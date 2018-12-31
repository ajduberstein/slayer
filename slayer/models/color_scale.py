from collections import OrderedDict
from warnings import warn

from .scales.colors import DEFAULT_PALETTES, get_random_rgb
from .scales.breaks import calculate_breaks
from .scales.interpolate import interpolate


class ColorScale(object):
    """
    Inspired by the way QGIS handles colors
    """

    def __init__(
        self,
        column,
        palette,
        scale_type='quantile'
    ):
        # Set palette
        if isinstance(palette, str) and palette in DEFAULT_PALETTES.keys():
            self.palette = DEFAULT_PALETTES[palette]
        elif isinstance(palette, list):
            self.palette = palette
        else:
            raise Exception('`palette` must be a `list` of RGB values or a `str` indicating one of a list '
                            'of common palettes.')

        if scale_type in ('categorical', 'categorical_random'):
            self.breaks = _process_categorical_variables(self.column, scale_type, self.palette)
        else:
            # TODO add type check
            self.breaks = calculate_breaks(column, scale_type)
        self.gradient_lookup = self.produce_gradient()

    @classmethod
    def produce_gradient(cls):
        gradient = []
        for i, lower_bound in enumerate(cls.breaks):
            break_percentage = float(i) / len(cls.breaks)
            gradient.append(interpolate(cls.palette, break_percentage))
        return OrderedDict(zip(cls.breaks, gradient))

    def get_gradient_lookup(self):
        return self.gradient_lookup


def _process_categorical_variables(data, scale_type, palette):
    # Choose from a common gradient
    classes = sorted(list(set(data)))
    if scale_type == 'categorical' and len(classes) > len(palette):
        warn('Number of categories for the specified column is greater '
             'than the number of colors available in the color palette. '
             'The legend will contain duplicate colors.')
    for i, c in enumerate(classes):
        if scale_type == 'categorical':
            color = palette[i % len(c)]
        elif scale_type == 'categorical_random':
            color = get_random_rgb()

    return OrderedDict([(d, color) for i, d in enumerate(classes)])
