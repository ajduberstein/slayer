from __future__ import print_function

import slimit

from slayer.string_utils import suppress_stderr


def check_js_equal(expected=None, actual=None):
    """Minify the JavaScript and compare it"""
    with suppress_stderr():
        print('Minifying expected JS')
        js0 = slimit.minify(expected)
        print('Minifying actual JS')
        js1 = slimit.minify(actual)
    if js0 == js1:
        return True
    print('Expected')
    print(js0)
    print('Actual')
    print(js1)
    return False
