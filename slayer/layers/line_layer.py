from ..models import Layer

from ..models.get_functions import (
    make_js_get_radius,
    make_js_get_source_position,
    make_js_get_target_position
)


class LineLayer(Layer):

    def __init__(
        self,
        data,
        radius_field='radius',
        source_position_field='start',
        target_position_field='end',
        **kwargs
    ):
        super(LineLayer, self).__init__(data, **kwargs)
        self.get_radius = make_js_get_radius(radius_field)
        self.get_source_position = make_js_get_source_position(source_position_field)
        self.get_target_position = make_js_get_target_position(target_position_field)
        self.get_stroke_width = 3

        # Remove unusable attributes
        delattr(self, 'get_position')
