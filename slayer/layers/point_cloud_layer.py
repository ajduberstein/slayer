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

    Example usage of underlying JS is here:
    https://github.com/uber/deck.gl/blob/334d38f93c3246208ccd88a3205b9971a99b3dfd/examples/gallery/src/point-cloud-layer.html

    """
    def __init__(
        self,
        data,
        radius_pixels=4,
        position=['x', 'y', 'z'],
        coordinate_system='COORDINATE_SYSTEM.IDENTITY',
        normal=[0, 0, 1],
        color=ORANGE_RGB,
        time_field=None,
        **kwargs
    ):
        super(PointCloudLayer, self).__init__(data, **kwargs)
        self.get_position = make_js_get_position(position)
        if isinstance(color, ColorScale):
            color.set_data(self.data)
        self.color = color
        self.time_field = time_field
        self.get_color = make_js_get_color(color, use_time=self.time_field)
        self.get_normal = make_js_get_normal(normal)
        self.radius_pixels = radius_pixels
        self.coordinate_system = coordinate_system

        # TODO don't hardcode this
        self.light_settings = '''
          {
            coordinateSystem: COORDINATE_SYSTEM.IDENTITY,
            lightsPosition: [20, 100, 100, 50, 0, 0],
            lightsStrength: [1, 0, 2, 0],
            numberOfLights: 2,
            ambientRatio: 0.2
          }'''.strip()
