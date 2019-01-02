# -*- coding: utf-8 -*-
"""
Test Scale Calculations
------------
"""
from collections import OrderedDict

from slayer.models.color_scale import ColorScale


import pandas as pd


df = pd.DataFrame({
    'number': [3.118, 7.132, 9.621, 3.253, 3.678, 4.63, 3.253, 9.128, 1.722, 0.455],
    'category': ['home', 'sign_up', 'search', 'search', 'search', 'home', 'home', 'search', 'sign_up', 'search']
})


def test_numerical_color_scale():
    scale = ColorScale(
        variable_name='number',
        data=df,
        num_classes=5,
        palette=[[229, 245, 249], [44, 162, 95]],
        scale_type='quantile')

    gradient = scale.get_gradient_lookup()

    EXPECTATION_KEYS = [0.455, 2.8388, 3.253, 4.0588, 7.5312]
    EXPECTATION_VALUES = [
        [229, 245, 249],
        [192.0, 228.4, 218.2],
        [155.0, 211.8, 187.4],
        [118.0, 195.2, 156.60000000000002],
        [81.0, 178.6, 125.8]]
    assert EXPECTATION_KEYS == gradient.keys()
    assert EXPECTATION_VALUES == gradient.values()


def test_categorical_color_scale():
    scale = ColorScale(
        variable_name='category',
        data=df,
        palette=[
            [102, 194, 165],
            [252, 141, 98],
            [141, 160, 203],
            [231, 138, 195],
            [166, 216, 84],
            [255, 217, 47],
            [229, 196, 148],
            [179, 179, 179]
        ],
        scale_type='categorical')

    gradient = scale.get_gradient_lookup()
    expectation = OrderedDict([
        ('home', [102, 194, 165]),
        ('search', [252, 141, 98]),
        ('sign_up', [141, 160, 203]),
    ])
    assert expectation.keys() == gradient.keys()
    assert expectation.values() == gradient.values()
