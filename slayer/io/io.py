from __future__ import print_function

import os
import os.path
import jinja2
import tempfile
import time
import webbrowser

from IPython.display import IFrame


TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '../templates/')
j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH),
                            trim_blocks=True)


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
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


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


def display_html(html_str, filename=None):
    """Converts HTML into a temporary file and open it in the system browser
        or IPython/Jupyter Notebook IFrame.

    Args:
        html_str (str): String of HTML to render
        filename (str): Local name of file
    """
    f = None
    try:
        if is_cli():
            f = open_named_or_temporary_file(filename)
            f.write(html_str)
            path = os.path.realpath(f.name)
            url = 'file://{}'.format(path)
            # Hack to prevent blank page
            time.sleep(1)
            webbrowser.open(url)
        elif in_ipynb():
            f = open_named_or_temporary_file(filename=filename, dir=os.getcwd())
            f.write(html_str)
            local_name = f.name.split('/')[-1]
            return IFrame(local_name, height=500, width=500)
        else:
            return html_str
    except Exception as e:
        raise(e)
    finally:
        if f is not None:
            f.close()


def open_named_or_temporary_file(filename='', dir=''):
    if filename:
        filename = add_html_extension(filename)
        return open(filename, 'w+')
    if dir:
        return tempfile.NamedTemporaryFile(
            suffix='.html', dir=dir, delete=False)
    return tempfile.NamedTemporaryFile(
        suffix='.html', delete=False)


def add_html_extension(fname):
    if fname.endswith('.html') or fname.endswith('.htm'):
        return fname
    if fname is None:
        raise Exception("File has no name")
    return fname + '.html'
