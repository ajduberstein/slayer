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
        ipynb_imports(html_str)
        return
    else:
        return html_str


def ipynb_imports(html):
    # TODO support lazy loading of libraries
    display(HTML(
        '''
        <script type="text/javascript">
        require.config({
          paths: {
            "deck.gl": "https://unpkg.com/deck.gl@latest/deckgl.min.js",
            "mapbox-gl": "https://api.tiles.mapbox.com/mapbox-gl-js/v0.44.1/mapbox-gl.js"
          }
        });
        require(["d3", "topojson", "cloud"], function(d3, topojson, cloud){
            window["deck"] = d3;
        });
        </script>
        '''))
