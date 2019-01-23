from __future__ import absolute_import

from ..models import Layer

from ..models.get_functions import (
    make_js_get_color,
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
        **kwargs
    ):
        super(HexagonLayer, self).__init__(data, **kwargs)
        self.radius = int(radius)
        self.get_position = make_js_get_position(position)
        if isinstance(color, ColorScale):
            color.set_data(self.data)
        self.get_color = make_js_get_color(color, time_field=self.time_field)
        self.pickable = 'true'
        self.extruded = 'true'
        self.elevation_scale = float(4)
