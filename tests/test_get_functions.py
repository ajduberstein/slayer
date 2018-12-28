from slayer.layers.get_functions import (
    get_stroke_width
)


def test_get_stroke_width():
    assert get_stroke_width('stroke') == 'function(x) { return x["stroke"] }'


def test_make_js_func_for():
    test_table = [
        ['color', 'list', [255, 0, 0],'function (x) { return x["color"] || [255, 0, 0] }'],
        ['color', 'list', None, 'function (x) { return x["color"] || [255, 0, 0] }'],
        ['size', 'float', 1., None, 'function (x) { return x["color"] || 1.000000 }'],
    ]

    for test_set in test_table:
        assert _make_js_func_for(test_set[0], test_set[1], test_set[2]) == test_set[3]


COLORS = ['#f1eef6', '#d0d1e6', '#a6bddb', '#74a9cf', '#2b8cbe', '#045a8d']
CATEGORICAL_DATA = 'cat dog'.split()
CATEGORICAL_DATA_LONG = ['cat'] * 4 + ['dog'] * 12
NUMERIC_DATA = [0, 2.5, 7.5]
NUMERIC_DATA_LONG = range(0, 100)
NUMERIC_DATA_RUNIF = [951, 7, 307, 158, 959, 951, 795, 559, 869, 770]


def test_categorical_color_scale():
    assert get_categorical_scale(COLORS, CATEGORICAL_DATA) == {'cat': '#f1eef6', 'dog': '#74a9cf'}
    assert get_categorical_scale(COLORS, CATEGORICAL_DATA_LONG) == {'cat': '#f1eef6', 'dog': '#74a9cf'}


def test_equal_interval_color_scale():
    assert get_equal_interval_scale(COLORS, CATEGORICAL_DATA)
    assert get_equal_interval_scale(COLORS, NUMERIC_DATA) == OrderedDict([
            (0, '#f1eef6'), (2.5, '#a6bddb'), (5, '#2b8cbe')])
    assert get_equal_interval_scale(COLORS, NUMERIC_DATA_LONG) == OrderedDict([
            (0, '#f1eef6'),
            (17, '#d0d1e6'),
            (34, '#a6bddb'),
            (51, '#74a9cf'),
            (68, '#2b8cbe'),
            (85, '#045a8d')])

    with pytest.raises(TypeError) as excinfo:
        assert get_equal_interval_scale(COLORS, CATEGORICAL_DATA) == {'cat': '#f1eef6', 'dog': '#74a9cf'}


def test_quantile_color_scale():
    assert get_quantile_scale(COLORS, NUMERIC_DATA_RUNIF) == OrderedDict([
        (7, ''),
        (307, ''),
        (770, ''),
        (869, ''),
        (951, '')
    ])

    with pytest.raises(TypeError) as excinfo:
        assert get_quantile_scale(COLORS, CATEGORICAL_DATA) == {'cat': '#f1eef6', 'dog': '#74a9cf'}




