from ..models import Layer
from ..models.get_functions import make_js_get_radius


class Scatterplot(Layer):

    def __init__(
        self,
        data,
        radius_field='radius',
        **kwargs
    ):
        super(Scatterplot, self).__init__(data, **kwargs)
        if radius_field:
            self.get_radius = make_js_get_radius(radius_field, default_val=100)
