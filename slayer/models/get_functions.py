from .color_scale import ColorScale


# TODO Handle with Jinja instead
CONST_TEMPLATE = 'return %s;'
STR_CONST_TEMPLATE = 'return "%s";'
FIELD_TEMPLATE = 'return x["%s"];'
CONDITIONAL_TEMPLATE = '%s;'


def wrap_js_func(func):
    def wrapper(*args, **kwargs):
        return 'function (x) { %s }' % func(*args, **kwargs)
    return wrapper

@wrap_js_func
def make_js_get_position(position_field_names):
    if len(position_field_names) == 2 and isinstance(position_field_names, list):
        return 'return [x["%s"], x["%s"]]' % (position_field_names[0], position_field_names[1])
    elif isinstance(position_field_names, str):
        return FIELD_TEMPLATE % position_field_names


@wrap_js_func
def make_js_get_color(color, time_field=None):
    """Converts color field or value to JS string for processing in browser

        Arguments: color (`str`, `list` of `float`, or `slayer.ColorScale`): If string,
                a hex value for the color all visualized items in the layer should have.
                If a list, the same as previous, given as an RGB value in a list.
                Otherwise a color scale.

        Returns :
            str: Executable JavaScript meant for embedding in deck.gl object.
    """
    func_pieces = []
    if time_field:
        js_filter = ('if (timeFilter > x["%s"]) {'
                     '    return [0, 0, 0, 0];'
                     '}')
        js_filter = js_filter % (time_field)
        func_pieces.append(js_filter)

    if isinstance(color, str) and color.startswith('#'):
        # Hex value
        # TODO convert to hex
        func_pieces.append(CONST_TEMPLATE % color)
    elif isinstance(color, str):
        # Color field name
        func_pieces.append(FIELD_TEMPLATE % color)
    elif isinstance(color, list) and len(color) in (3, 4):
        # RGBA value
        func_pieces.append(CONST_TEMPLATE % color)
    elif isinstance(color, ColorScale):
        lookup = color.get_gradient_lookup()
        conditional_str = _make_deckgl_conditional(
            lookup.keys(), lookup.values(), color.variable_name
        )
        func_pieces.append(CONDITIONAL_TEMPLATE % conditional_str)
    func = '\n'.join(func_pieces)
    return func
    # TODO support custom ranges
    # if isinstance(color, OrderedDict):
    # Also enable categorical colors
    # if isinstance(color, dict):


@wrap_js_func
def make_js_get_radius(radius_field_or_value):
    if isinstance(radius_field_or_value, float) or isinstance(radius_field_or_value, int):
        return CONST_TEMPLATE % radius_field_or_value
    if isinstance(radius_field_or_value, str):
        return FIELD_TEMPLATE % radius_field_or_value


def _safe_get(arr, idx, default=None):
    try:
        return arr[idx]
    except IndexError:
        return default


def _make_deckgl_conditional(breaks_list, characteristic_list, attr_name):
    """Creates a JS conditional statement for use in deck.gl functions"""
    js_pieces = []
    js_conditional_template = 'else if (%s <= x["%s"] && x["%s"] < %s)\n\t{\n\treturn %s}\n'
    characteristic_list = list(characteristic_list)
    breaks_list = list(breaks_list)
    i = 0
    while i < len(breaks_list):
        if_statement = js_conditional_template % (
            breaks_list[i],
            attr_name,
            attr_name,
            _safe_get(breaks_list, i + 1, 'Infinity'),
            characteristic_list[i])
        js_pieces.append(if_statement)
        i += 1
    return _cut_first_else('\n'.join(js_pieces))


def _cut_first_else(string):
    return string.replace('else', '', 1).strip()
