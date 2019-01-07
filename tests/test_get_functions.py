from slayer.models.get_functions import (
    make_js_get_position,
    make_js_get_color,
    _safe_get
)

from slayer.models import ColorScale

from .utils import check_js_equal


def test_safe_get():
    assert _safe_get([0, 1], 2, 1) == 1
    assert _safe_get([0, 1], 1, 0) == 1


def test_make_js_get_color():
    assert make_js_get_color([255, 255, 255]) == 'function (x) { return [255, 255, 255]; }'
    assert make_js_get_color([255, 255, 255, 0]) == 'function (x) { return [255, 255, 255, 0]; }'

    FAKE_DATA = [{'comitates': i} for i in range(0, 10)]
    color_js = make_js_get_color(
            ColorScale(data=FAKE_DATA, variable_name='comitates', palette='BuPu', num_classes=2))
    EXPECTATION = (
            'function (x) {'
            '  if (0.0 <= x["comitates"] && x["comitates"] < 4.5) {'
            '    return [224.0, 236.0, 244.0];'
            '  } else if (4.5 <= x["comitates"] && x["comitates"] < Infinity) {'
            '    return [180.0, 161.0, 205.5];'
            '  }'
            '}')
    print(color_js)
    assert check_js_equal(EXPECTATION, color_js)


def test_make_js_get_position():
    assert make_js_get_position('coordinates') == 'function (x) { return x["coordinates"]; }'
