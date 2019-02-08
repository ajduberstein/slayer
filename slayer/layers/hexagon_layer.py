from __future__ import absolute_import

from ..models import Layer

from ..models.get_functions import (
    make_js_get_elevation_value,
    make_js_get_position
)

from ..models.color_scale import produce_numerical_gradient
from ..models.scales.colors import DEFAULT_PALETTES


class HexagonLayer(Layer):

    def __init__(
        self,
        data,
        position=['lng', 'lat'],
        radius=1000,
        color_range='OrRd',
        elevation=None,
        elevation_scale=None,
        pickable=True,
        extruded=True,
        elevation_domain=None,
        num_colors=6,
        **kwargs
    ):
        super(HexagonLayer, self).__init__(data, **kwargs)
        self.radius = int(radius)
        self.get_position = make_js_get_position(position)
        self.color_range = self._resolve_color_range(color_range, num_colors)
        self.pickable = 'true' if pickable else 'false'
        self.extruded = 'true' if extruded else 'false'
        self.get_elevation_value = make_js_get_elevation_value(elevation, self.time_field)
        self.elevation_scale = len(self.data) / float(self.radius) if elevation_scale is None else elevation_scale
        self.elevation_domain = str(elevation_domain) if elevation_domain else '[0, %s]' % len(self.data)
        self.color = None

    def _resolve_color_range(self, color_range, num_colors):
        palette_names = DEFAULT_PALETTES.keys()
        if isinstance(color_range, str) and color_range in palette_names:
            breaks_list = range(0, num_colors)
            palette = DEFAULT_PALETTES[color_range]
            return str(list(produce_numerical_gradient(breaks_list, palette).values()))
        if isinstance(color_range, list):
            return color_range
        raise TypeError(
            '`color_range` must be a string indicating a ColorBrewer '
            'palette or a `list` of RGBA values. Valid palettes: '
            ', '.join(palette_names))
