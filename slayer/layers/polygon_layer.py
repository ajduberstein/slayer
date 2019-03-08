from __future__ import absolute_import

from ..models import Layer
from ..models.get_functions import (
    make_js_get_color,
    make_js_get_elevation,
    get_value_or_field,
)

from ..models import ColorScale


ORANGE_RGB = [255, 127, 0]
TRANSPARENT_RGBA = [0, 0, 0, 0]


class PolygonLayer(Layer):
    """Plot countours"""

    def __init__(
        self,
        data,
        line_width=1,
        polygon='polygon',
        elevation=0,
        fill_color=ORANGE_RGB,
        line_color=TRANSPARENT_RGBA,
        **kwargs
    ):
        super(PolygonLayer, self).__init__(data, **kwargs)
        if isinstance(fill_color, ColorScale):
            fill_color.set_data(self.data)
        if line_color and not isinstance(line_color, (str, list)):
            raise TypeError('line_color must be a string indicating a field name, or a list representing an RGBA value')
        self.line_color = get_value_or_field(line_color, types_to_check=(list))
        self.fill_color = make_js_get_color(fill_color)
        self.get_line_width = get_value_or_field(line_width)
        self.get_elevation = make_js_get_elevation(elevation)
        self.get_polygon = get_value_or_field(polygon, types_to_check=(list))
