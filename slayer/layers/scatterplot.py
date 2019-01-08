from __future__ import absolute_import

from ..models import Layer
from ..models.get_functions import (
    make_js_get_color,
    make_js_get_position,
    make_js_get_radius
)
from ..models import ColorScale


ORANGE_RGB = [255, 127, 0, 166]


class Scatterplot(Layer):
    """Geographic scatterplot

        Args:
            radius (float): Radius size of a point
            position (str): Column name in `data` that indicates a datum's position

                If `data` has a separate x and y column, both should be specified in a list,
                like `position=['lng', 'lat']`, otherwise a single string name should be
                provided, like `position='coordinates'`.

                Position is specified in (x, y) coordinate pairs--that is,
                lat-lon pairs should be listed as with longitude first,
                since longitude is the horizontal/x-axis value.

            color (`slayer.ColorScale`, `str`, or `list` of `float`): Desired color for data points, passabl
                as a hex string, RGB array, or `ColorScale` object for more detailed plots.

    """

    def __init__(
        self,
        data,
        position=['lat', 'lng'],
        radius=100000.0,
        color=ORANGE_RGB,
        **kwargs
    ):
        super(Scatterplot, self).__init__(data, **kwargs)
        self.get_position = make_js_get_position(position)
        self.get_radius = make_js_get_radius(radius)
        if isinstance(color, ColorScale):
            color.set_data(self.data)
        self.get_color = make_js_get_color(color, time_field=self.time_field)
