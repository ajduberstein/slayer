from collections import OrderedDict
from warnings import warn

from .scales.colors import DEFAULT_PALETTES, get_random_rgb
from .scales.breaks import calculate_breaks, VALID_SCALES
from .scales.interpolate import interpolate


class ColorScale(object):
    """
    Inspired by the way QGIS handles colors
    """

    def __init__(
        self,
        variable_name=None,
        palette=None,
        scale_type='quantile',
        data=None
    ):
        # Set palette
        if isinstance(palette, str) and palette in DEFAULT_PALETTES.keys():
            self.palette = DEFAULT_PALETTES[palette]
        elif isinstance(palette, list):
            self.palette = palette
        else:
            raise Exception('`palette` must be a `list` of RGB values or a `str` indicating one of a list '
                            'of common palettes.')

        if not isinstance(variable_name, str):
            raise Exception('`variable_name` must be a string represented in the data set headers.')
        self.variable_name = variable_name

        if scale_type not in VALID_SCALES:
            raise Exception('`scale_type` must be one of the following: %s' % ', '.join(VALID_SCALES))
        self.scale_type = scale_type

    def produce_gradient(self):
        gradient = []
        for i, lower_bound in enumerate(self.breaks):
            break_percentage = float(i) / len(self.breaks)
            gradient.append(interpolate(self.palette, break_percentage))
        return OrderedDict(zip(self.breaks, gradient))

    def set_data(self, data):
        self.data = [d[self.variable_name] for d in data]
        if self.scale_type in ('categorical', 'categorical_random'):
            self.breaks = _process_categorical_variables(self.data, self.scale_type, self.palette)
        else:
            # TODO add type check
            self.breaks = calculate_breaks(self.data, self.scale_type)
        self.gradient_lookup = self.produce_gradient()

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
