from ..models import Layer
from ..models.get_functions import (
    make_js_get_position,
    make_js_get_radius,
)


class Scatterplot(Layer):
    """Geographic scattersplot

        Args:
            radius_field (float): Radius size of a point
            position_field (str): Column name in `data` that indicates a datum's position

                If `data` has a separate x and y column, both should be specified in a list,
                like `position_field=['lng', 'lat']`, otherwise a single string name should be
                provided, like `position_field='coordinates'`.

                Position is specified in (x, y) coordinate pairs--that is,
                lat-lon pairs should be listed as with longitude first, since longitude is the horizontal x value.

    """

    def __init__(
        self,
        data,
        position_field=['lat', 'lng'],
        radius_field='radius',
        radius_default=10,
        **kwargs
    ):
        super(Scatterplot, self).__init__(data, **kwargs)
        self.get_position = make_js_get_position(position_field)
        self.get_radius = make_js_get_radius(radius_field, default_val=radius_default)
