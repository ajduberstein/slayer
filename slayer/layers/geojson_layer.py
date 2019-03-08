from __future__ import absolute_import

import json

from ..models import Layer
from ..models.get_functions import (
    make_js_get_color,
    make_js_get_elevation
)
from ..models import ColorScale
from ..io import geojson_to_pandas_df


ORANGE_RGB = [255, 127, 0]


class GeoJsonLayer(Layer):
    """GeoJSON plotting layer

        Args:
            data (str): GeoJSON FeatureCollection. If you'd like to use Well-Known Text (WKT),
                check out PolygonLayer.
            fill_color (:obj:`slayer.ColorScale`, :obj:`str`, or :obj:`list` of :obj:`float`):
                Desired color for data points, passable as a hex string,
                RGB array, or `ColorScale` object for more detailed plots.
            line_color (:obj:`slayer.ColorScale`, :obj:`str`, or :obj:`list` of :obj:`float`):
                Desired color for data points, passable as a hex string,
                RGB array, or `ColorScale` object for more detailed plots.
    """

    def __init__(
        self,
        geojson,
        line_color=ORANGE_RGB,
        fill_color=ORANGE_RGB,
        elevation=0,
        **kwargs
    ):
        input_json_dict = validate_json(geojson)
        self.display_data = input_json_dict
        self.data = geojson_to_pandas_df(input_json_dict)
        super(GeoJsonLayer, self).__init__(self.data, **kwargs)
        if isinstance(fill_color, ColorScale):
            fill_color.set_data(self.data)
        if isinstance(line_color, ColorScale):
            line_color.set_data(self.data)
        self.line_color = make_js_get_color(line_color)
        self.fill_color = make_js_get_color(fill_color)
        # TODO support more than one color field
        self.color = self.fill_color
        self.get_elevation = make_js_get_elevation(elevation)


def validate_json(myjson):
    if isinstance(myjson, str):
        return json.loads(str(myjson))  # noqa
    elif isinstance(myjson, dict):
        return myjson
