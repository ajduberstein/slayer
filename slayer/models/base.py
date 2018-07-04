class RenderMixin(object):
    def render(self):
        NotImplementedError("Class %s doesn't implement render()" % (self.__class__.__name__))


class AbstractDeckBase(object):
    pass
