from color_scale import ColorScale


CONST_TEMPLATE = 'function (x) { return %s }'
STR_CONST_TEMPLATE = 'function (x) { return "%s" }'
FIELD_TEMPLATE = 'function (x) { return x["%s"] }'
CONDITIONAL_TEMPLATE = 'function (x) { %s }'


def make_js_get_position(position_field_names):
    if len(position_field_names) == 2:
        return 'function (x) { return [x["%s"], x["%s"]] }' % (position_field_names[0], position_field_names[1])
    return FIELD_TEMPLATE % position_field_names


def make_js_get_color(color):
    """Converts color field or value to JS string for processing in browser

        Arguments:
            color (`str`, `list` of `float`, or `slayer.ColorScale`): If string,
                a hex value for the color all visualized items in the layer should have.
                If a list, the same as previous, given as an RGB value in a list.
                Otherwise a color scale.

        Returns :
            str: Executable JavaScript meant for embedding in deck.gl object.
    """
    if isinstance(color, str) and color.startswith('#'):
        # Hex value
        return CONST_TEMPLATE % color  # TODO convert to hex
    if isinstance(color, str):
        # Color field name
        return FIELD_TEMPLATE % color
    if isinstance(color, list) and len(color) in (3, 4):
        # RGBA value
        return CONST_TEMPLATE % color
    if isinstance(color, ColorScale):
        lookup = color.get_gradient_lookup()
        conditional_str = _make_deckgl_conditional(
            lookup.keys(), lookup.values(), color.variable_name
        )
        return CONDITIONAL_TEMPLATE % conditional_str
    # TODO support custom ranges
    # if isinstance(color, OrderedDict):
    # Also enable categorical colors
    # if isinstance(color, dict):


def make_js_get_radius(radius_field_or_value):
    if isinstance(radius_field_or_value, float) or isinstance(radius_field_or_value, int):
        return CONST_TEMPLATE % radius_field_or_value
    if isinstance(radius_field_or_value, str):
        return FIELD_TEMPLATE % radius_field_or_value


def safe_get(arr, idx, default=None):
    try:
        return arr[idx]
    except IndexError:
        return default


def _make_deckgl_conditional(breaks_list, characteristic_list, attr_name):
    """Creates a JS conditional statement for use in deck.gl functions"""
    js_pieces = []
    js_conditional_template = 'else if (%s <= x["%s"] && x["%s"] < %s)\n\t{\n\treturn %s}\n'
    i = 0
    while i < len(breaks_list):
        if_statement = js_conditional_template % (
            breaks_list[i],
            attr_name,
            attr_name,
            safe_get(breaks_list, i + 1, 'Infinity'),
            characteristic_list[i])
        js_pieces.append(if_statement)
        i += 1
    return _cut_first_else('\n'.join(js_pieces))


def _cut_first_else(string):
    return string.replace('else', '', 1).strip()
