from contextlib import contextmanager
import os
import sys
import textwrap


def dedent_strip(s):
    return textwrap.dedent(s).strip()


@contextmanager
def suppress_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr
