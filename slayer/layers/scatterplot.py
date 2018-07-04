from ..models import Layer


class Scatterplot(Layer):

    def __init__(
        self,
        data,
        radius_field='radius',
        **kwargs
    ):
        super(Scatterplot, self).__init__(data, **kwargs)
        if radius_field:
            self.get_radius = 'function (x) { return x["%s"] || 100 }' % radius_field
