import jinja2


from .base import ViewportInterface


class OrbitView(ViewportInterface):
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
        fov=50,
        zoom=10,
        rotation_x=-30,
        rotation_orbit=30,
        rotation_axis='Y',
        distance=10,
        min_distance=1,
        max_distance=20,
    ):
        super(OrbitView, self).__init__()
        self.fov = fov
        self.rotation_x = rotation_x
        self.rotation_orbit = rotation_orbit
        self.rotation_axis = rotation_axis
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.distance = distance
        self.zoom = zoom

    def render(self):
        template = jinja2.Template((
            'var INITIAL_VIEW_STATE = {'
            '    distance: {{distance}},'
            '    rotationX: {{rotation_x}},'
            '    rotationOrbit: {{rotation_orbit}},'
            '    zoom: {{zoom}},'
            '    fov: {{fov}},'
            '    minDistance: {{min_distance}},'
            '    maxDistance: {{max_distance}}}'))
        return template.render(**self.to_dict())

    def to_dict(self):
        return {
            "fov": self.fov,
            "rotation_x": self.rotation_x,
            "rotation_orbit": self.rotation_orbit,
            "rotation_axis": self.rotation_axis,
            "zoom": self.zoom,
            "distance": self.distance,
            "min_distance": self.min_distance,
            "max_distance": self.max_distance}
