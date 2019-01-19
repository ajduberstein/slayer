from __future__ import absolute_import

from ..models import Layer

from ..models.get_functions import (
    make_js_get_radius,
    make_js_get_color
)


ORANGE_RGB = [255, 127, 0]


class HexagonLayer(Layer):

    def __init__(
        self,
        data,
        position=['lat', 'lng'],
        radius='radius',
        color=ORANGE_RGB,
        **kwargs
    ):
        super(HexagonLayer, self).__init__(data, **kwargs)
        self.get_radius = make_js_get_radius(radius)
        self.get_color = make_js_get_color(color, time_field=self.time_field)
