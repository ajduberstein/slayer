class RenderInterface(object):
    def render(self):
        raise NotImplementedError("Class %s doesn't implement render()" % (self.__class__.__name__))


class ViewportInterface(object):
    def to_dict(self):
        raise NotImplementedError("Class %s doesn't implement to_dict()" % (self.__class__.__name__))

    def render(self):
        raise NotImplementedError("Class %s doesn't implement render()" % (self.__class__.__name__))

    def autocompute(self):
        raise NotImplementedError("Class %s doesn't implement autocompute()" % (self.__class__.__name__))
