from __future__ import absolute_import

from ..models import Layer
from ..models.get_functions import (
    make_js_get_position,
    make_js_get_color
)
from ..models import ColorScale


ORANGE_RGB = [255, 127, 0]
TRANSPARENT_RGBA = [0, 0, 0, 0]


class PolygonLayer(Layer):
    """Plot countours"""

    def __init__(
        self,
        data,
        lineWidthMinPixels=1,
        polygon='contour',
        elevation=0,
        fill_color=ORANGE_RGB,
        line_color=TRANSPARENT_RGBA,
        line_width=1,
        **kwargs
    ):
        super(PolygonLayer, self).__init__(data, **kwargs)
        self.get_polygon = make_js_get_position('contour')
        if isinstance(fill_color, ColorScale):
            fill_color.set_data(self.data)
        self.fill_color = make_js_get_color(fill_color, time_field=self.time_field)
        if isinstance(line_color, ColorScale):
            line_color.set_data(self.data)
        self.line_color = make_js_get_color(line_color, time_field=self.time_field)
