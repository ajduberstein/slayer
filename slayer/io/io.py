from __future__ import print_function

import os
import os.path
import jinja2
import tempfile
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


def display_html(html_str, filename=''):
    """Converts HTML into a temporary file and open it in the system browser
    Args:
        html_str (str): String of HTML to render
    """
    cwd = os.getcwd() if in_ipynb() or is_cli() else None
    f = get_file(filename, cwd)
    try:
        f.write(html_str)
        if is_cli() and filename is None:
                path = f.name
                url = path
                if not in_ipynb:
                    webbrowser.open(url)
        elif in_ipynb():
            local_name = f.name.split('/')[-1]
            return IFrame(local_name, height=500, width=500)
        else:
            return html_str
    except Exception as e:
        raise(e)
    finally:
        if f is not None:
            f.close()


def get_file(filename, dir=None):
    f = None
    # Temporary file in cwd, usually
    if filename is None and dir is not None:
        f = tempfile.NamedTemporaryFile(suffix='.html', prefix='slayer_', dir=dir, delete=False)
    # Temporary file
    elif filename is None and dir is None:
        f = tempfile.NamedTemporaryFile(suffix='.html', prefix='slayer_', delete=False)
    else:
        path = os.path.join(dir, add_html_extension(filename)) if dir else add_html_extension(filename)
        f = open(path, 'w+')
    return f


def add_html_extension(fname):
    if fname.endswith('.html') or fname.endswith('.htm'):
        return fname
    if fname is None:
        raise Exception("File has no name")
    return fname + '.html'
