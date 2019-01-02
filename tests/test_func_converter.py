# -*- coding: utf-8 -*-
"""
Test Python Function Converter
------------
"""

import pytest

from slayer import func_converter
from slayer.string_utils import dedent_strip


MULTILINE = 'def f(x):\n    return x * x'


def f(x):
    return x * x


def test_strip_if_anon():
    assert func_converter.strip_if_anon('lambda x: x') == 'lambda x: x'
    assert func_converter.strip_if_anon('func_to_str(lambda x: x)') == 'lambda x: x'


def test_verify_compilation():
    # Test failure
    with pytest.raises(func_converter.FunctionInvalidException):
        func_converter.verify_compilation('lamba x: x')
        incorrect_multiline_func = (
            'def f(x):'
            '   rerun x'
        )
        func_converter.verify_compilation(incorrect_multiline_func)
    # Test success  -- expect no exceptions
    try:
        func_converter.verify_compilation('lambda: x')
        func_converter.verify_compilation(MULTILINE)
    except Exception as e:
        pytest.fail("Unexpected error in test", e)


CORRECT_MULTILINE = dedent_strip("""
def switchy_mcswitchstatement(x):
    if x == 1:
        return 'h'
    elif x == 2:
        return 'e'
    else:
        return 'y'""")


def test_func_to_str():
    assert func_converter.func_to_str(lambda x: x) == 'lambda x: x'
    assert func_converter.func_to_str(f) == MULTILINE

    def switchy_mcswitchstatement(x):
        if x == 1:
            return 'h'
        elif x == 2:
            return 'e'
        else:
            return 'y'
    assert func_converter.func_to_str(switchy_mcswitchstatement) == CORRECT_MULTILINE


def test_str_to_js():
    expected = "function switchy_mcswitchstatement(x) {\n    if (x == 1) {\n        return 'h';\n    } else if (x == 2) {\n        return 'e';\n    } else {\n        return 'y';\n\n    }\n}"  # noqa
    assert expected == func_converter.str_to_js(CORRECT_MULTILINE)
