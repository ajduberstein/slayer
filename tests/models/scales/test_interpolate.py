# -*- coding: utf-8 -*-
"""
Test Scale Calculations
------------
"""
from slayer.models.scales.interpolate import (
    _interpolate,
    interpolate
)


def test__interpolate():
    assert _interpolate([255, 0, 0], [128, 128, 128], 0.5) == [191.5, 64.0, 64.0]


def test_interpolate():
    actual = interpolate(
        [[255, 0, 0], [128, 128, 128], [128, 128, 256]], 0.25)
    assert actual == [191.5, 64.0, 64.0]
