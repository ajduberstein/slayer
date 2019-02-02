LEGEND_DEFAULT = {
    'font-family': 'monospace',
    'z-index': 500,
    'background-color': 'white',
    'position': 'absolute',
    'right': '10px',
    'bottom': '30px',
    'padding': '5px',
    'overflow-x': 'auto',
    'overflow-y': 'auto',
}

TOOLTIP_DEFAULT = {
    'font-family': 'monospace',
    'position': 'absolute',
    'z-index': 1,
    'pointer-events': 'none',
    'display': 'none',
    'background-color': 'white',
    'padding': '1vw',
}

class Style(object):
    def __init__(
        self,
        legend=LEGEND_DEFAULT,
        tooltip=TOOLTIP_DEFAULT
    ):
        self.legend = legend
        self.tooltip = tooltip

    def get_css(self, attr_name):
        obj_to_render = self.__dict__[attr_name]
        return dict_to_css(obj_to_render)


def dict_to_css(d):
    css_str = ''
    css_row = '{}: {};\n'
    for k, v in d.items():
        css_str += css_row.format(k, v)
    return css_str
