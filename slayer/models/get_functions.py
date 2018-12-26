ORANGE_RGB = [255, 127, 0]


def make_js_get_position(position_field_names):
    if len(position_field_names) == 2:
        return 'function (x) { return [x["%s"], x["%s"]] }' % (position_field_names[0], position_field_names[1])
    return 'function (x) { return x["%s"] }'


def _make_js_func_for(field_name, return_type, default_val=None):
    if not default_val:
        return 'function (x) { return x["%s"] }'
    if return_type == 'str':
        return 'function (x) { return x["%s"] || %s }' % (field_name, str(default_val))
    if return_type == 'float':
        return 'function (x) { return x["%s"] || %f }' % (field_name, default_val)


def get_stroke_width(stroke_width_field_name, default_val=10):
    return _make_js_func_for(stroke_width_field_name, 'str', default_val)


def make_js_get_source_position(source_position_field_name):
    return _make_js_func_for(source_position_field_name)


def make_js_get_target_position(target_position_field_name):
    return _make_js_func_for(target_position_field_name)


def make_js_get_color(color_field_name, color_scale_list, default_val=ORANGE_RGB):
    return _make_js_func_for(color_field_name, 'str', default_val)


def make_js_get_radius(radius_field_name, default_val=100):
    return _make_js_func_for(radius_field_name, 'float', default_val)
