from __future__ import absolute_import

from ..models import Layer
from ..models.get_functions import (
    make_js_get_position,
    make_js_get_color,
    make_js_get_normal
)
from ..models import ColorScale


ORANGE_RGB = [255, 127, 0]


class PointCloudLayer(Layer):
    """Plot a point cloud, as are often seen in self-driving visualizations

        Args:
            fill_color (:obj:`slayer.ColorScale`, :obj:`str`, or :obj:`list` of :obj:`float`):
                Desired color for data points, passable as a hex string,
                RGB array, or `ColorScale` object for more detailed plots.
            line_color (:obj:`slayer.ColorScale`, :obj:`str`, or :obj:`list` of :obj:`float`):
                Desired color for data points, passable as a hex string,
                RGB array, or `ColorScale` object for more detailed plots.

    """
    def __init__(
        self,
        data,
        radiusPixels=4,
        position='position',
        normal=[0, 0, 1],
        color=ORANGE_RGB,
        **kwargs
    ):
        super(PointCloudLayer, self).__init__(data, **kwargs)
        self.get_position = make_js_get_position(position)
        if isinstance(color, ColorScale):
            color.set_data(self.data)
        self.get_color = make_js_get_color(color, time_field=self.time_field)
        self.get_normal = make_js_get_normal(normal)
