from __future__ import print_function

import os
import os.path
import tempfile


def get_file_or_tempfile(fname=''):
    if not fname:
        return tempfile.NamedTemporaryFile(suffix='.html', delete=False)
    if not os.path.isfile(fname):
        raise IOError("File already exists at %s" % fname)
    return open(fname, 'w+')
