from __future__ import absolute_import

import uuid

from camel_snake_kebab import camelCase
import jinja2
import pandas as pd

from .base import RenderInterface
from .color_scale import ColorScale


VALID_LAYER_KEYWORDS = {
    'id',
    'visible',
    'opacity',
    'pickable',
    'on_hover',
    'data',
    'on_click',
    'get_color',
    'get_position',
    'elevation_scale',
    'get_radius',
    'radius',
    'color_range',
    'extruded',
    'get_start_position',
    'get_fill_color',
    'get_elevation_value',
    'get_text',
    'radius_pixels',
    'text_anchor',
    'get_size',
    'get_angle',
    'get_text_anchor',
    'get_alignment_base',
    'get_elevation_base',
    'elevation_domain',
    'line_width',
    'get_normal',
    'get_end_position',
    'get_line_color',
    'get_line_width',
    'highlight_color',
    'highlighted_object_index',
    'auto_highlight',
    'light_settings',
    'coordinate_system',
    'coordinate_origin',
    'model_matrix',
    'update_triggers'}


class Layer(RenderInterface):
    """Base layer and parent to all Layers, handling DOM output

        Args:
            data (:obj:`list` of :obj:`dict`): Data to be plotted, ideally as a Pandas DataFrame
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
        time_field=None,
        min_time=None,
        max_time=None,
        pickable=True,
        opacity=1,
        title='',
        js_function_overrides={}
    ):
        super(Layer, self).__init__()
        if not isinstance(data, pd.DataFrame):
            data = pd.from_dict(data, orient='records')
        self.data = data
        class_name = self.__class__.__name__
        # Layer name for deck.gl
        self.layer_type = class_name if 'Layer' in self.__class__.__name__ else class_name + 'Layer'
        self.js_function_overrides = js_function_overrides
        self.title = ''
        self.pickable = 'true' if pickable else 'false'
        self.id = '"%s"' % uuid.uuid4()

        if time_field is not None:
            try:
                times = data[time_field]
            except KeyError:
                raise Exception("Data does not have a time field named `%s`" % time_field)
            self.update_triggers = "{getColor: [timeFilter], getElevationValue: [timeFilter]}"
        self.time_field = time_field
        self.min_time = min(times) if time_field else None
        self.max_time = max(times) if time_field else None

        self.opacity = float(opacity)

    def _join_attrs(self):
        """Joins valid object attributes to populate a DeckGL layer object's
        arguments in the JavaScript template.

        For example, `get_position`, `data`, and `get_color` would become

        ```
        getPosition: {{ get_position }},
        getColor: {{ get_color }}
        data: {{ data }},
        ```

        which will then be called by `render`
        """
        deckgl_chart_args = []
        for attr in self.__dict__.keys():
            if attr not in VALID_LAYER_KEYWORDS:
                continue
            js_func_str = self.js_function_overrides.get(attr) or '{{ %s }}' % attr
            deckgl_chart_arg = '{named_arg}: {js_func}'.format(named_arg=camelCase(attr), js_func=js_func_str)
            if attr == 'data':
                chart_data = self.data.to_json(orient='records', date_format='iso')
                deckgl_chart_arg = '{named_arg}: {data}'.format(
                    named_arg='data', data=chart_data)
            deckgl_chart_args.append(deckgl_chart_arg)
        return ',\n'.join(deckgl_chart_args)

    def render(self):
        template = jinja2.Template(
            'new {{ layer_type }}({' + self._join_attrs() + '})')
        return template.render(**self.__dict__)

    def add_to(self, slayer):
        """Adds map layer to a Slayer object

        Inspired by `add_to` in Folium, see examples at https://bit.ly/2KGbgxK

        Args:
            slayer (:obj`slayer.Slayer`): spatial layer wrapper object
        """
        slayer + self

    def get_legend(self):
        """Gets a color-based legend"""
        if isinstance(self.color, ColorScale):
            return self.color.get_gradient_lookup(for_display=True)
        if isinstance(self.color, dict):
            return self.color
        return None

    def get_color_field(self):
        if isinstance(self.color, ColorScale):
            return self.color.variable_name
        if isinstance(self.color, str):
            return self.color

    def get_color_lookup(self):
        if isinstance(self.color, ColorScale):
            return self.color
