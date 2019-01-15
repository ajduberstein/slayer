from __future__ import absolute_import

import jinja2

from .base import RenderMixin
from ..data_utils.viewport_helpers import (
    bbox_to_zoom_level,
    geometric_mean,
    get_bbox,
    get_n_pct
)


class Viewport(RenderMixin):
    def __init__(
        self,
        latitude=0.0,
        longitude=0.0,
        zoom=0,
        pitch=0,
        bearing=0,
        max_zoom=None
    ):
        super(Viewport, self).__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom
        self.max_zoom = zoom
        self.pitch = pitch
        self.bearing = bearing

    def to_json(self):
        return {
            "bearing": self.bearing,
            "dragRotate": False,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "pitch": self.pitch,
            "zoom": self.zoom,
            "isSplit": False}

    def render(self):
        template = jinja2.Template('''
     var INITIAL_VIEWPORT_STATE = {
       latitude: {{ latitude }},
       longitude: {{ longitude }},
       zoom: {{ zoom }},
       pitch: {{ pitch }},
       bearing: {{ bearing }}
     }''')
        return template.render(**self.to_json())

    @classmethod
    def autocompute(cls, points, view_propotion=1):
        bbox = get_bbox(get_n_pct(points, view_propotion))
        zoom = bbox_to_zoom_level(bbox)
        center = geometric_mean(points)
        return cls.__init__(latitude=center[1], longitude=center[0], zoom=zoom)
