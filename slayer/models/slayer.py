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
        viewport (:obj:`Viewport`): Viewport that defines the angle at which the user
            observes the layers
    """

    def __init__(
        self,
        viewport,
        layers=None,
        mapbox_api_key=None,
    ):
        self.viewport = viewport
        self._layers = layers or []
        self.mapbox_api_key = mapbox_api_key

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

    def to_html(self, interactive=False):
        """Converts all layers and viewport objects into HTML

        If interactive and in a CLI, attempts to open a web browser

        If interactive via an ipynb, emits results to the output cell

        Returns:
            str: Rendered HTML from Jinja template
        """
        rendered_layers = self.compile_layers()
        rendered_viewport = self.viewport.render()
        html = j2_env.get_template('body.htm').render(
                header=j2_env.get_template('header.htm').render(),
                footer=j2_env.get_template('footer.htm').render(),
                layers=rendered_layers,
                viewport=rendered_viewport,
                mapbox_api_key=self.mapbox_api_key,
                interactive=interactive)
        if interactive:
            return display_html(html)
