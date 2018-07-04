from camel_snake_kebab import camelCase
import jinja2
import pandas as pd

from .base import RenderMixin


class Layer(RenderMixin):

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
        'get_radius',
        'highlight_color',
        'highlighted_object_index',
        'auto_highlight',
        'coordinate_system',
        'coordinate_origin',
        'model_matrix',
        'update_triggers'}

    def __init__(
        self,
        data,
        latitude_field='latitude',
        longitude_field='longitude',
        color_field='color',
        layer_name=None,
    ):
        super(Layer, self).__init__()
        if isinstance(data, pd.DataFrame):
            data = data.to_json(orient='records')
        self.data = data
        self.get_position = 'function (x) { return [x["%s"], x["%s"]] }' % (longitude_field, latitude_field)
        self.get_color = 'function (x) { return x["%s"] || [0, 0, 0] }' % (color_field)
        self.layer_type = self.__class__.__name__ + 'Layer'

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
            if attr not in self.VALID_LAYER_KEYWORDS:
                continue
            js_chart_args.append(
                '\n\t\t%s: {{ %s }}' % (camelCase(attr), attr))
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
