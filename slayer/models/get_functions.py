from .models.color_scale import ColorScale
ORANGE_RGB = [255, 127, 0]


def make_js_get_position(position_field_names):
    if len(position_field_names) == 2:
        return 'function (x) { return [x["%s"], x["%s"]] }' % (position_field_names[0], position_field_names[1])
    return 'function (x) { return x["%s"] }'


def _make_js_func_for(field_name, return_type, default_val=None):
    if not default_val:
        return 'function (x) { return x["%s"] }'
    if return_type in ('str', 'list'):
        return 'function (x) { return x["%s"] || %s }' % (field_name, str(default_val))
    if return_type == 'float':
        return 'function (x) { return x["%s"] || %f }' % (field_name, default_val)


def get_stroke_width(stroke_width_field_name):
    return _make_js_func_for(stroke_width_field_name, 'float')


def make_js_get_source_position(source_position_field_name):
    return _make_js_func_for(source_position_field_name)


def make_js_get_target_position(target_position_field_name):
    return _make_js_func_for(target_position_field_name)


def make_js_get_color(color=ORANGE_RGB, color_scale_list=[]):
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
        return _make_js_func_for('color', 'str', default_val=color)
    if isinstance(color, list) and len(color) in (3, 4):
        return _make_js_func_for('color', 'str', default_val=color)
    if isinstance(color, ColorScale):
        conditional_str = _make_deckgl_conditional(
            color.get_breaks(), color.get_gradient()
        )
        return 'function (x) { %s }' % conditional_str
    # TODO support custom ranges
    # if isinstance(color, OrderedDict):
    # Also enable categorical colors
    # if isinstance(color, dict):


def make_js_get_radius(radius_field_or_value):
    if isinstance(radius_field_or_value, float):
        return _make_js_func_for('radius', 'float', radius_field_or_value)
    return _make_js_func_for(radius_field_or_value, 'float')


def _make_deckgl_conditional(breaks_list, characteristic_list):
    """Creates a JS conditional statement for use in deck.gl functions"""
    js_pieces = []
    prev_break = breaks_list[0]
    i = 1
    js_conditional_template = 'else if ({lower_bound} <= x < {upper_bound})\n\t{\n\treturn {mapped_scale_value}}\n'
    for current_break in breaks_list[1:]:
        if_statement = js_conditional_template.format(
            lower_bound=prev_break,
            upper_bound=current_break,
            mapped_scale_value=characteristic_list[i])
        js_pieces.append(if_statement)
        i += 1
    return _cut_first_else(js_conditional_template)


def _cut_first_else(string):
    return string.replace('else', '').strip()
