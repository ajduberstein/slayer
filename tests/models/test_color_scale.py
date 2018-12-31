# -*- coding: utf-8 -*-
"""
Test Scale Calculations
------------
"""
from collections import OrderedDict

from slayer.models.color_scale import ColorScale
from slayer.models.scale.colors import DEFAULT_PALETTES


NUMERICAL_DATA = [3.118, 7.132, 9.621, 3.253, 3.678, 4.63, 3.253, 9.128, 1.722, 0.455]
CATEGORICAL_DATA = ['home', 'sign_up', 'search', 'search', 'search', 'home']


def test_numerical_color_scale():
    scale = ColorScale(NUMERICAL_DATA, [[229, 245, 249], [44, 162, 95]])
    gradient = scale.get_gradient_lookup()
    expectation = OrderedDict([
        (0.455, [229, 245, 249]),
        (3.118, []),
        (3.253, []),
        (4.63, []),
        (9.128, [44, 162, 95])])
    assert expectation.keys() == gradient.keys()
    assert expectation.values() == gradient.values()


def test_categorical_color_scale():
    scale = ColorScale(
        CATEGORICAL_DATA, DEFAULT_PALETTES['set1'], scale_type='categorical')
    gradient = scale.get_gradient_lookup()
    expectation = OrderedDict([
        ('home', []),
        ('search', []),
        ('sign_up', []),
    ])
    assert expectation.keys() == gradient.keys()
    assert expectation.values() == gradient.values()
