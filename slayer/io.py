from __future__ import print_function

import os
import os.path
import tempfile
import webbrowser
from IPython.core.display import display, HTML


def get_file_or_tempfile(fname=''):
    if not fname:
        return tempfile.NamedTemporaryFile(suffix='.html', delete=False)
    if not os.path.isfile(fname):
        raise IOError("File already exists at %s" % fname)
    return open(fname, 'w+')


def in_ipynb():
    """Detects if package is running in iPython Notebook

    https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook

    Returns:
        bool: True if in ipynb
    """
    try:
        cfg = get_ipython().config
        if cfg['IPKernelApp']['parent_appname'] == 'ipython-notebook':
            return True
        else:
            return False
    except NameError:
        return False


def is_interactive():
    """Detects if package is running interactively

    https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook

    Returns:
        bool: True if session is interactive
    """
    import __main__ as main
    return not hasattr(main, '__file__')


def is_cli():
    """Detects if app is running in CLI (e.g., `ipython`, `python`)

    Returns:
        bool: True if session is interactive and on CLI
    """
    return not in_ipynb() and is_interactive()


def display_html(html_str):
    """Converts HTML into a temporary file and open it in the system browser

    Args:
        html_str (str): String of HTML to render
    """
    if is_cli():
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
            path = f.name
            url = 'file://' + path
            f.write(html_str)
        webbrowser.open(url)
        return
    elif in_ipynb():
        display(HTML(html_str))
        return
    else:
        return html_str
