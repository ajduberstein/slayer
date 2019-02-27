import jinja2
import textwrap


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


def strip_and_dedent(func):
    def wrapper(*args, **kwargs):
        return textwrap.dedent(func(*args, **kwargs).strip())
    return wrapper


@strip_and_dedent
def make_js_get_position(position_field_names):
    is_list = isinstance(position_field_names, list)

    POSITION_FUNCTION_TEMPLATE = jinja2.Template('''
      function (x) {
        return [

        {%- for p in position_field_names if is_list %}
          x["{{position_field_names[loop.index0]}}"]{{ '];' if loop.last else ',' }}

        {%- else -%}

        return x["{{position_field_names}}"];
        {% endfor %}
      }'''.strip())

    return POSITION_FUNCTION_TEMPLATE.render(
        is_list=is_list,
        position_field_names=position_field_names)


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
    # TODO support custom ranges
    # if isinstance(color, OrderedDict):
    # Also enable categorical colors
    # if isinstance(color, dict):
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
        func_pieces.append(
            'return COLOR_LOOKUP["{variable}"].get(x["{variable}"]);'.format(variable=color.variable_name))
    func = '\n'.join(func_pieces)
    return func


def make_js_get_radius(radius_field_or_value):
    return get_value_or_field(radius_field_or_value)


def make_js_get_normal(normal_field_or_value):
    return get_value_or_field(normal_field_or_value, types_to_check=(list))


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


def make_js_get_elevation(elevation_value_or_field):
    return get_value_or_field(elevation_value_or_field)


@strip_and_dedent
def get_value_or_field(value_or_field, types_to_check=(float, int)):
    """Returns either a single value or JavaScript function returning a named field

    In order to not end up writing JavaScript in Python, we let the programmer decide
    between returning a named value from the underlying data or a constant.

    Arguments:
        value_or_field: Field name or constant to return.
        types_to_check (tuple): List of types that make the `value_or_field` parameter treated as a constant.

    Returns:
        str: deck.gl layer parameter
    """

    is_value = isinstance(value_or_field, types_to_check)
    TEMPLATE = jinja2.Template("""
    {%- if is_value %}
    {{value_or_field}}
    {% else -%}

    function(x) {
      return x["{{value_or_field}}"];
    }
    {%- endif %}
    """)
    return TEMPLATE.render(is_value=is_value, value_or_field=value_or_field)
