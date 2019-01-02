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
    if is_cli():
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
            path = f.name
            url = path
            f.write(html_str)
            if not in_ipynb:
                webbrowser.open(url)
    elif in_ipynb():
            cwd = os.getcwd()
            f = None
            if filename is None:
                f = tempfile.NamedTemporaryFile(suffix='.html', prefix='slayer_', dir=cwd, delete=False)
            else:
                path = os.path.join(cwd, make_html_file(filename))
                f = open(path, 'w+')
            try:
                f.write(html_str)
                local_name = f.name.split('/')[-1]
                return IFrame(local_name, height=500, width=500)
            finally:
                if f is not None:
                    f.close()
    else:
        return html_str


def make_html_file(fname):
    if fname.endswith('.html') or fname.endswith('.htm'):
        return fname
    return fname + '.html'
