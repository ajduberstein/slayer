from camel_snake_kebab import camelCase
import jinja2
import pandas as pd

from .base import RenderMixin
from .get_functions import (
    make_js_get_color,
    make_js_get_position
)

VALID_LAYER_KEYWORDS = {
    'id',
    'visible',
    'opacity',
    'pickable',
    'on_hover',
    'data',
    'on_click',
    'get_position',
    'get_color',
    'highlight_color',
    'highlighted_object_index',
    'auto_highlight',
    'coordinate_system',
    'coordinate_origin',
    'model_matrix',
    'update_triggers'}


class Layer(RenderMixin):
    """Base layer and parent to all Layers, handling DOM output

        Args:
            data (:obj:`list` of :obj:`dict`): Data to be plotted, ideally as a Pandas DataFrame
            position_field (str): Column name in `data` that indicates a datum's position

                If `data` has a separate x and y column, both should be specified in a list,
                like `position_field=['lng', 'lat']`, otherwise a single string name should be
                provided, like `position_field='coordinates'`.

                Please be mindful that position is specified in an (x, y)--lat-lon pairs should
                be listed as (lon, lat), since longitude is a horizontal or x value.
            color_field (`str`): Column name that specifies an data entry's color
            js_function_overrides (:obj:`dict` of :obj`(str, str)`): Dictionary that allows the user to
                specify JS functions for more control of behavior in deck.gl.

                For example, to get fine control of the `get_color` function, one
                may consider specifying a dictionary like:

                ```
                js_function_overrides={
                    'get_color': 'function(d) { [Math.random() * 255, 0, Math.random() * 255, 255] }'
                }
                ```
    """

    def __init__(
        self,
        data,
        position_field=['longitude', 'latitude'],
        color_field='color',
        js_function_overrides={},
    ):
        super(Layer, self).__init__()
        if isinstance(data, pd.DataFrame):
            data = data.to_json(orient='records')
        self.data = data
        self.get_position = make_js_get_position(position_field)
        self.get_color = make_js_get_color(color_field)
        class_name = self.__class__.__name__
        self.layer_type = class_name if 'Layer' in self.__class__.__name__ else class_name + 'Layer'
        self.valid_layer_keywords = VALID_LAYER_KEYWORDS
        self.js_function_overrides = js_function_overrides

    def _join_attrs(self):
        """Joins valid object attributes to populate a DeckGL layer object's
        arguments in the JavaScript template.

        For example, `get_position`, `data`, and `get_color` would become

        ```
        getPosition: {{ get_position }},
        data: {{ data }},
        getColor: {{ get_color }}
        ```

        which will then be called by `render`

        """
        js_chart_args = []
        for attr in self.__dict__.keys():
            if attr not in self.valid_layer_keywords:
                continue
            js_func_str = self.js_function_overrides.get(attr) or attr
            js_chart_args.append(
                '\n\t\t%s: {{ %s }}' % (camelCase(attr), js_func_str))
        return ','.join(js_chart_args)

    def render(self):
        template = jinja2.Template(
          'new {{ layer_type }}({' +
          self._join_attrs() + '})')
        return template.render(**self.__dict__)

    def add_to(self, slayer):
        """Adds map layer to a Slayer object

        Inspired by `add_to` in Folium, see examples at https://bit.ly/2KGbgxK

        Args:
            slayer (:obj`slayer.Slayer`): spatial layer wrapper object
        """
        slayer + self
