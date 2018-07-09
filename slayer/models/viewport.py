import jinja2


from .base import RenderMixin


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

    def render(self):
        template = jinja2.Template('''
     var INITIAL_VIEWPORT_STATE = {
       latitude: {{ latitude }},
       longitude: {{ longitude }},
       zoom: {{ zoom }},
       pitch: {{ pitch }}
     }''')
        return template.render(
            latitude=self.latitude,
            longitude=self.longitude,
            zoom=self.zoom,
            pitch=self.pitch
        )
