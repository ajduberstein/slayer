# -*- coding: utf-8 -*-
"""
Test Scale Calculations
------------
"""
from slayer.models.scales import (
    _interpolate,
    interpolate
)


def test__interpolate():
    assert _interpolate([255, 0, 0], [128, 128, 128], 0.5) == [191.5, 64.0, 64.0]


def test_interpolate():
    assert interpolate(
        [[255, 0, 0], [128, 128, 128], [128, 128, 256]], 0.25) == [191.5, 64.0, 64.0]
