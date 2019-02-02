from __future__ import absolute_import

import os.path
import jinja2

from .layer import Layer
from .viewport import Viewport
from .style import Style
from ..io import (
    display_html,
    open_named_or_temporary_file
)


TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '../templates/')
j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
                            trim_blocks=True)


class Slayer(object):
    """Spatial layer container object, defining global aspects of the map

    Attributes:
        layers (:obj:`list` of :obj:`Layer`): Layers to be plotted on a map
        viewport (:obj:`slayer.Viewport`): Viewport that defines the angle at which the user
            observes the layers. If nothing is passed, the Viewport will be autocomputed off
            the first-passed layer.
        mapbox_api_key (:obj:`str`, optional): Public API key from Mapbox.
            Can be passed as MAPBOX_API_KEY environment variable.
            Tokens can be found at https://www.mapbox.com/account/access-tokens
    """

    def __init__(
        self,
        viewport=None,
        layers=None,
        style=None,
        add_legend=True,
        mapbox_api_key=None,
        blend=False,
        drag_boxes=True,
        add_tooltip=True,
    ):
        self.viewport = viewport
        self._layers = layers or []
        self._style = style or Style()
        self.add_legend = add_legend
        self.mapbox_api_key = mapbox_api_key or os.environ.get('MAPBOX_API_KEY')
        self.blend = blend
        self.add_timer = False
        self.drag_boxes = drag_boxes
        self.add_tooltip = add_tooltip

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
        """Computes attributes across layers"""
        layers = []
        self.min_time = float('inf')
        self.max_time = float('-inf')
        for layer in self._layers:
            layers.append(layer.render())
            self.add_timer = layer.time_field or self.add_timer
            self.min_time = min(layer.min_time, self.min_time)
            self.max_time = max(layer.max_time, self.max_time)
        return ',\n'.join(layers)

    def to_html(self, filename=None, interactive=False, html_only=False, js_only=False):
        """Converts all layers and viewport objects into HTML

        Args:
            filename (str): Filename to write HTML to. If none is passed, an HTML string
                will be returned.
            interactive (bool): Set to True if running in Jupyter or Python terminal.
                Slayer will open the file in a web browser or, if Jupyter, an iframe.
            js_only (bool): Returns only a portion of the compiled JS, for testing & development.

        Returns:
            str: Rendered HTML
        """
        rendered_layers = self.compile_layers()
        rendered_viewport = self.render_viewport()
        legend = self._layers[0].get_legend() if self.add_legend else None
        color_field = self._layers[0].get_color_field() if self.add_legend else None
        js = j2_env.get_template('js.j2').render(
            layers=rendered_layers,
            viewport=rendered_viewport,
            blend=self.blend,
            add_tooltip=self.add_tooltip,
            mapbox_api_key=self.mapbox_api_key)
        if js_only:
            return js
        html = j2_env.get_template('body.j2').render(
            add_timer=self.add_timer,
            min_time=self.min_time,
            max_time=self.max_time,
            add_tooltip=self.add_tooltip,
            color_field=color_field,
            legend=legend,
            style=self._style,
            js=js,
            drag_boxes=self.drag_boxes)
        if interactive:
            return display_html(html, filename=filename)
        if html_only:
            return html
        with open_named_or_temporary_file(filename) as f:
            f.write(html)

    def render_viewport(self):
        """Renders the JS for a deck.gl Viewport object

        If no Viewport has been passed, Slayer will autocompute
        a Viewport for the first layer of data.

        Returns:
            str: Viewport JS string
        """
        if self.viewport is not None:
            return self.viewport.render()
        return Viewport.autocompute(self._layers[0])
