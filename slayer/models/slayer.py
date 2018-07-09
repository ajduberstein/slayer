import os.path
import jinja2

from slimit.parser import Parser

from .layer import Layer
from .viewport import Viewport
from ..io import display_html
from ..string_utils import suppress_stderr


TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '../templates/')

j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
                            trim_blocks=True)


class Slayer(object):
    """Spatial layer container object, defining global aspects of the map

    Attributes:
        layers (:obj:`list` of :obj:`Layer`): Layers to be plotted on a map
        viewport (:obj:`slayer.Viewport`): Viewport that defines the angle at which the user
            observes the layers
        mapbox_api_key (:obj:`str`, optional): Public API key from Mapbox
    """

    def __init__(
        self,
        viewport,
        layers=None,
        mapbox_api_key=None,
    ):
        self.viewport = viewport
        self._layers = layers or []
        self.mapbox_api_key = os.environ.get('MAPBOX_API_KEY') or mapbox_api_key

    def __add__(self, obj):
        """Appends a Layer or creates a Viewport

        ggplot2-inspired operator overload

        Args:
            obj (:obj`Layer` or :obj`Viewport`): Layers or viewport to be
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
        layers = [layer.render() for layer in self._layers]
        return ',\n'.join(layers)

    def to_html(self, interactive=False, js_only=True, validate_js=False):
        """Converts all layers and viewport objects into HTML

        If interactive and in a CLI, attempts to open a web browser

        If interactive via an ipynb, emits results to the output cell

        Args:
            interactive (bool): Should be True if running in iPython or Jupyter
            js_only (bool): Should be True if the user wants to return only the
                compiled JS
            validate_js (bool): Not yet implemented. Should be True if user wants to validate that
                the JS rendered to the DOM is valid ES5 JavaScript.

        Returns:
            str: Rendered HTML from Jinja template
        """
        rendered_layers = self.compile_layers()
        rendered_viewport = self.viewport.render()
        js = j2_env.get_template('js.j2').render(
                layers=rendered_layers,
                viewport=rendered_viewport,
                mapbox_api_key=self.mapbox_api_key,
                interactive=interactive)
        if js_only:
            return js
        header = j2_env.get_template('header.j2').render(),
        footer = j2_env.get_template('footer.j2').render(),
        html = j2_env.get_template('body.j2').render(
            header=header,
            js=js,
            footer=footer,
        )
        if interactive:
            return display_html(html)
        return html


def check_syntax(js_str):
    """Checks for valid JS ES5 syntax

        Throws an exception if the syntax is invalid

        Exists to help catch errors before DOM rendering

        Args:
            js_str (str): String of JavaScript to check
    """
    try:
        with suppress_stderr():
            parser = Parser()
            parser.parse(js_str)
    except SyntaxError as e:
        raise SyntaxError('User-provided JS is not valid ES5: %s' % e)
