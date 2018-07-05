import ast
import json
import re
import textwrap


from dill.source import getsource
import jiphy
from yapf.yapflib.yapf_api import FormatCode
import js2py


"""
Reasons for this module:
1) I don't want the end-user writing JavaScript. Preferably you have to know nothing about JS
to use this library.
2) I do want the flexibility granted by deck.gl's get{Color,Position} functions
3) It's not that hard to implement a Python function to JS function library
"""


class FunctionInvalidException(Exception):
    pass


class UnsupportedException(Exception):
    pass


def verify_compilation(python_code_str):
    try:
        exec(compile(ast.parse(python_code_str), filename='<ast>', mode='exec'))
    except Exception:
        raise FunctionInvalidException(
            "Given function is not valid Python: %s" % python_code_str)


def func_to_str(f):
    source = getsource(f)
    func_str = textwrap.dedent(strip_if_anon(source))
    verify_compilation(func_str)
    return func_str.strip()


def func_to_js(f):
    if is_lambda(f):
        raise UnsupportedException("lambda functions not yet supported. Use a closure instead.")
    return str_to_js(func_to_str(f))


def verify_js_equals_pyfunc(pyfunc, jsfunc, js_func_name, datum):
    datum = json.loads(datum)
    js = 'function() {\n\t'
    js += js2py(jsfunc)
    js += '\n\tvar datum = {};'.format(datum)
    js += '\n\treturn {}(datum)}'.format(js_func_name)
    js_result = js2py.eval_js(js)
    py_result = pyfunc(datum)
    if js_result == py_result:
        return (True, js_result, py_result)
    return (False, js_result, py_result)


def str_to_js(python_str):
    formatted_str = FormatCode(python_str)[0]
    return jiphy.to.javascript(formatted_str).strip()


def strip_if_anon(func_str):
    rex = re.search(r'func_to_str\((.+)\)', func_str)
    if rex:
        return rex.group(1)
    return func_str


def is_lambda(v):
    LAMBDA = lambda: 0  # noqa
    return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__
