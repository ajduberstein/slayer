import ast
import re
import textwrap


from dill.source import getsource
import jiphy
from yapf.yapflib.yapf_api import FormatCode


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
        raise UnsupportedException("Lambdas not supported. Use a closure instead.")
    return str_to_js(func_to_str(f))


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
