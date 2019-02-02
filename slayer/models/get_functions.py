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
    if time_field is not None:
        js_filter = ('if (x["%s"] > timeFilter) {'
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
        conditional_str = ''
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


def _make_deckgl_conditional(breaks_list, characteristic_list, attr_name):
    """Creates a JS conditional statement for use in deck.gl functions"""
    js_pieces = []
    is_categorical = type(list(breaks_list)[-1]) == str
    js_conditional_template = _get_js_conditional_template(is_categorical)
    characteristic_list = list(characteristic_list)
    breaks_list = list(breaks_list)
    i = 0
    while i < len(breaks_list):
        parameters_tup = _get_parameters_tup(i, breaks_list, attr_name, characteristic_list, is_categorical)
        if_statement = js_conditional_template % parameters_tup
        js_pieces.append(if_statement)
        i += 1
    return _cut_first_else('\n'.join(js_pieces))


def _get_js_conditional_template(is_categorical):
    if is_categorical:
        js_conditional_template = 'else if (\'%s\' === x["%s"]) {  return %s; }'
    else:
        js_conditional_template = 'else if (%s <= x["%s"] && x["%s"] < %s) {  return %s; }'
    return js_conditional_template


def _get_parameters_tup(idx, breaks_list, attr_name, characteristic_list, is_categorical):
    if is_categorical:
        parameters_tup = (breaks_list[idx], attr_name, characteristic_list[idx])
    else:
        parameters_tup = (
            breaks_list[idx],
            attr_name,
            attr_name,
            _safe_get(breaks_list, idx + 1, 'Infinity'),
            characteristic_list[idx])
    return parameters_tup


def _cut_first_else(string):
    return string.replace('else', '', 1).strip()


@wrap_js_func
def make_js_return_const(const):
    if isinstance(const, str):
        return STR_CONST_TEMPLATE % const
    return CONST_TEMPLATE % const
