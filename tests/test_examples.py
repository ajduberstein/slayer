# -*- coding: utf-8 -*-
"""
Test Examples
------------

Verify that all examples run without a syntax error

Does not guarantee that the output is logical
"""

import pytest

import subprocess

def test_examples():
    subprocess.check_output(['python', './examples/scatterplot.py'])
    subprocess.check_output(['python', './examples/scatterplot_over_time.py'])
    subprocess.check_output(['python', './examples/hexagon_layer.py'])
    assert True
