from __future__ import absolute_import

from ..models import Layer
from ..models.get_functions import (
    make_js_get_color,
    make_js_get_position,
    make_js_get_radius,
    make_js_get_text,
    make_js_return_const
)
from ..models import ColorScale


ORANGE_RGB = [255, 127, 0]


class TextLayer(Layer):
    """Text annotations to plot on a map"""

    def __init__(
        self,
        data,
        position=['lng', 'lat'],
        size=32,
        text='name',
        text_anchor='middle',
        angle=0,
        alignment_baseline='center',
        color=ORANGE_RGB,
        **kwargs
    ):
        super(TextLayer, self).__init__(data, **kwargs)
        self.get_position = make_js_get_position(position)
        self.get_size = make_js_get_radius(size)
        self.get_angle = make_js_get_radius(angle)
        self.get_text_anchor = make_js_return_const(text_anchor)
        self.get_alignment_baseline = make_js_return_const(alignment_baseline)
        self.get_text = make_js_get_text(text)
        if isinstance(color, ColorScale):
            color.set_data(self.data)
        self.get_color = make_js_get_color(color, time_field=kwargs.get('time_field'))
