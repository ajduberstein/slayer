from __future__ import absolute_import

import os.path
import jinja2

from .layer import Layer
from .viewport import Viewport
from ..io import display_html


TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '../templates/')

j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
                            trim_blocks=True)


class Slayer(object):
    """Spatial layer container object, defining global aspects of the map

    Attributes:
        layers (:obj:`list` of :obj:`Layer`): Layers to be plotted on a map
        viewport (:obj:`slayer.Viewport`): Viewport that defines the angle at which the user
            observes the layers
        mapbox_api_key (:obj:`str`, optional): Public API key from Mapbox.
            Can be passed as MAPBOX_API_KEY environment variable.
    """

    def __init__(
        self,
        viewport=None,
        layers=None,
        legends=None,
        mapbox_api_key=None,
        blend=False,
    ):
        self.viewport = viewport
        self._layers = layers or []
        self._legends = legends or []
        self.mapbox_api_key = mapbox_api_key or os.environ.get('MAPBOX_API_KEY')
        self.blend = blend
        self.add_timer = False

    def __add__(self, obj):
        """Appends a Layer or creates a Viewport

        ggplot2-inspired operator overload

        Args:
            obj (:obj`Layer` or :obj:`Viewport`): Layers or viewport to be
                appended to the Slayer object
        """
        if isinstance(obj, Layer):
            self._layers.append(obj)
            return self
        elif isinstance(obj, Viewport):
            self.viewport = obj
            return self
        else:
            raise TypeError('+ is supported for Layer or Viewport objects only')

    def compile_layers(self):
        layers = []
        self.min_time = float('inf')
        self.max_time = float('-inf')
        for layer in self._layers:
            layers.append(layer.render())
            self.add_timer = layer.time_field or self.add_timer
            self.min_time = min(layer.min_time, self.min_time)
            self.max_time = max(layer.max_time, self.max_time)
            self.titles = layer.title
        return ',\n'.join(layers)

    def to_html(self, filename=None, interactive=False, js_only=False):
        """Converts all layers and viewport objects into HTML

        Args:
            js_only (bool): Should be True if the user wants to return only the
                compiled JS

        Returns:
            str: Rendered HTML
        """
        rendered_layers = self.compile_layers()
        rendered_viewport = self.viewport.render()
        js = j2_env.get_template('js.j2').render(
            layers=rendered_layers,
            viewport=rendered_viewport,
            blend=self.blend,
            mapbox_api_key=self.mapbox_api_key)
        if js_only:
            return js
        html = j2_env.get_template('body.j2').render(
            add_timer=self.add_timer,
            min_time=self.min_time,
            max_time=self.max_time,
            legends=self._legends or self._layers[0].get_legend(),
            js=js)
        if interactive:
            return display_html(html, filename=filename)
        if filename is None:
            return html
        with open(filename, 'w+') as f:
            f.write(filename)
