from __future__ import absolute_import

from math import log

from ..models import Layer

from ..models.get_functions import (
    make_js_get_color,
    make_js_get_elevation_value,
    make_js_get_position
)

from ..models import ColorScale

ORANGE_RGB = [255, 127, 0]


class HexagonLayer(Layer):

    def __init__(
        self,
        data,
        position=['lng', 'lat'],
        radius=1000,
        color=ORANGE_RGB,
        elevation=None,
        elevation_scale=None,
        pickable=True,
        extruded=True,
        **kwargs
    ):
        super(HexagonLayer, self).__init__(data, **kwargs)
        self.radius = int(radius)
        self.get_position = make_js_get_position(position)
        if isinstance(color, ColorScale):
            color.set_data(self.data)
        self.get_color = make_js_get_color(color, time_field=self.time_field)
        self.color = color
        self.pickable = 'true' if pickable else 'false'
        self.extruded = 'true' if extruded else 'false'
        self.get_elevation_value = make_js_get_elevation_value(elevation, self.time_field)
        self.elevation_scale = len(self.data) / float(self.radius) if elevation_scale is None else elevation_scale
        self.elevation_domain = '[0, %s]' % len(self.data)
