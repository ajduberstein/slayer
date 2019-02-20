from .color_scale import ColorScale


# TODO Handle with Jinja instead
CONST_TEMPLATE = 'return %s;'
STR_CONST_TEMPLATE = 'return "%s";'
FIELD_TEMPLATE = 'return x["%s"];'
CONDITIONAL_TEMPLATE = '%s'


def wrap_js_func(func):
    def wrapper(*args, **kwargs):
        return 'function (x) { %s }' % func(*args, **kwargs)
    return wrapper


@wrap_js_func
def make_js_get_position(position_field_names):
    if len(position_field_names) == 2 and isinstance(position_field_names, list):
        return 'return [x["%s"], x["%s"]]' % (position_field_names[0], position_field_names[1])
    if len(position_field_names) == 3 and isinstance(position_field_names, list):
        return 'return [x["%s"], x["%s"], x["%s"]]' % (
            position_field_names[0], position_field_names[1], position_field_names[2])
    elif isinstance(position_field_names, str):
        return FIELD_TEMPLATE % position_field_names


@wrap_js_func
def make_js_get_text(text_field_name):
    return FIELD_TEMPLATE % text_field_name


@wrap_js_func
def make_js_get_color(color, use_time=False):
    """Converts color field or value to JS string for processing in browser

        Arguments: color (`str`, `list` of `float`, or `slayer.ColorScale`): If string,
                a hex value for the color all visualized items in the layer should have.
                If a list, the same as previous, given as an RGB value in a list.
                Otherwise a color scale.

        Returns :
            str: Executable JavaScript meant for embedding in deck.gl object.
    """
    func_pieces = []
    if use_time:
        js_filter = ('if (x["__ts"] > timeFilter) {'
                     '    return [0, 0, 0, 0];'
                     '}')
        func_pieces.append(js_filter)

    if isinstance(color, str):
        # Color field name
        func_pieces.append(FIELD_TEMPLATE % color)
    elif isinstance(color, list) and len(color) in (3, 4):
        # RGBA value
        func_pieces.append(CONST_TEMPLATE % color)
    elif isinstance(color, ColorScale):
        # See interval_lookup.j2
<<<<<<< HEAD
        func_pieces.append(
            'return COLOR_LOOKUP["{variable}"].get(x["{variable}"]);'.format(variable=color.variable_name))
=======
        func_pieces.append('return COLOR_LOOKUP["{}"].get(x);'.format(color.variable_name))
>>>>>>> WIP use interval dictionary lookup
    func = '\n'.join(func_pieces)
    return func
    # TODO support custom ranges
    # if isinstance(color, OrderedDict):
    # Also enable categorical colors
    # if isinstance(color, dict):


def make_js_get_radius(radius_field_or_value):
    if isinstance(radius_field_or_value, (float, int)):
        return radius_field_or_value
    if isinstance(radius_field_or_value, str):
        return 'function(x) { return x["%s"]; }' % radius_field_or_value


@wrap_js_func
def make_js_get_normal(normal_field_or_value):
    if isinstance(normal_field_or_value, list):
        return CONST_TEMPLATE % normal_field_or_value
    if isinstance(normal_field_or_value, str):
        return FIELD_TEMPLATE % normal_field_or_value


def _safe_get(arr, idx, default=None):
    try:
        return arr[idx]
    except IndexError:
        return default


@wrap_js_func
def make_js_return_const(const):
    if isinstance(const, str):
        return STR_CONST_TEMPLATE % const
    return CONST_TEMPLATE % const


def make_js_get_elevation_value(elevation_value=None, use_time=False):
    if use_time:
        return '''
        function(points) {
            var boolFunc = function(d) { return d['__ts'] <= timeFilter }
            const elevation = points.filter(boolFunc).length
            return elevation;
        }'''.strip()

    if elevation_value is None:
        return 'function(points) { return points.length }'
