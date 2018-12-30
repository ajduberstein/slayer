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


def make_js_get_color(color_field_name, color_scale_list=[], default_val=ORANGE_RGB):
    return _make_js_func_for(color_field_name, 'str', default_val)


def make_js_get_radius(radius_field_name, default_val=100):
    return _make_js_func_for(radius_field_name, 'float', default_val)


def _make_deckgl_conditional(breaks_color_map):
    """Creates a JS conditional statement for use in deck.gl functions"""
    js_pieces = []
    prev_break = breaks_color_map[0]
    js_conditional_template = 'else if ({lower_bound} <= x < {upper_bound})\n\t{\n\treturn {mapped_scale_value}}\n'
    for current_break in breaks_color_map[1:]:
        if_statement = js_conditional_template.format(
            lower_bound=prev_break,
            upper_bound=current_break,
            mapped_scale_value=breaks_color_map)
        js_pieces.append(if_statement)
        pass


def _cut_first_else(string):
    return string.replace('else', '').strip()
