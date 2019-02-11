import jinja2


from .base import ViewportInterface


class OrbitView(ViewportInterface):
    """Configuration for data without an explicit need for a globe

    TODO reference deck.gl docs
    Attributes:
        fov (int): Contour of the field of vision
        zoom (int): Closeness to the center point of the data
        rotation_x (int): Initial X-axis rotation
        distance (int): Unit distance between points
    """
    def __init__(
        self,
        fov=10,
        zoom=1,
        rotation_x=0,
        rotation_orbit=0,
        orbit_axis='Y',
        distance=10,
        min_distance=1,
        max_distance=20
    ):
        super(OrbitView, self).__init__()
        self.fov = fov
        self.rotation_x = rotation_x
        self.rotation_orbit = rotation_orbit
        self.orbit_axis = orbit_axis
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.distance = distance
        self.zoom = zoom

    def render(self):
        template = jinja2.Template("""
        var INITIAL_VIEW_STATE = {
            distance: {{distance}},
            rotationX: {{rotation_x}},
            rotationOrbit: {{rotation_orbit}},
            orbitAxis: "{{orbit_axis}}",
            zoom: {{zoom}},
            fov: {{fov}},
            minDistance: {{min_distance}},
            maxDistance: {{max_distance}}
        }""")
        return template.render(**self.to_dict())

    def to_dict(self):
        return {
            "fov": self.fov,
            "rotation_x": self.rotation_x,
            "rotation_orbit": self.rotation_orbit,
            "orbit_axis": self.orbit_axis,
            "zoom": self.zoom,
            "distance": self.distance,
            "min_distance": self.min_distance,
            "max_distance": self.max_distance}
