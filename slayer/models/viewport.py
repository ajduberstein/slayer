from __future__ import absolute_import

import jinja2

import pandas as pd

from .base import RenderMixin
from ..data_utils.viewport_helpers import (
    bbox_to_zoom_level,
    geometric_mean,
    get_bbox,
    get_n_pct
)


class Viewport(RenderMixin):
    """Configuration for viewport for spatial data
    One can think of this as the camera that looks onto a the plane of data being plotted.

    Attributes:
        latitude (float): Latitude of the center of the viewport
        longitude (float): Longitude of the center of the viewport
        zoom (float): Zoom, ranging from 1-20 for a Mercator projection map. See also:
            https://gis.stackexchange.com/questions/7430/what-ratio-scales-do-google-maps-zoom-levels-correspond-to
        pitch (float): Tilt forward/backward of the viewport, in degrees.
        bearing (float): Swivel left/right of the viewport, in degrees.
    """
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

    def to_dict(self):
        return {
            "bearing": self.bearing,
            "dragRotate": False,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "pitch": self.pitch,
            "zoom": self.zoom,
            "isSplit": False}

    def render(self):
        template = jinja2.Template((
            'var INITIAL_VIEWPORT_STATE = {'
            '  latitude: {{ latitude }},'
            '  longitude: {{ longitude }},'
            '  zoom: {{ zoom }},'
            '  pitch: {{ pitch }},'
            '  bearing: {{ bearing }}'
            '}'))
        return template.render(**self.to_dict())

    @classmethod
    def autocompute(cls, points, view_proportion=0.95):
        """Automatically computes a zoom level for the points passed in.

        Args:
            points (:obj:`list` of :obj:`list` of :obj:`float` or :obj:`pandas.DataFrame`): A list of points
                in the form of `[[lng0, lat0], [lng1, lng0], ... , [lng_n, lat_n]]`.
            view_propotion (float): Proportion of the data that is meaningful to plot. Defaults to 95%.

        Returns:
            slayer.Viewport: Viewport fitted to the data
        """
        if isinstance(points, pd.DataFrame):
            points = points.to_records(index=False)
        bbox = get_bbox(get_n_pct(points, view_proportion))
        zoom = bbox_to_zoom_level(bbox)
        center = geometric_mean(points)
        instance = cls(latitude=center[1], longitude=center[0], zoom=zoom)
        return instance
