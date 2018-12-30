# -*- coding: utf-8 -*-
"""
Test Scale Calculations
------------
"""
from slayer.scales import (
    interpolate,
    calculate_percentile_breaks,
    calculate_equal_interval_breaks
)


def test_interpolate():
    assert interpolate([255, 0, 0], [128, 128, 128], 0.5) == [191.5, 64.0, 64.0]


def test_calculate_percentile_breaks():
    DATA = [0, 1, 1, 1, 3, 60, 3, 6]
    EXPECTATION = [0, 1.0, 3.0]
    assert calculate_percentile_breaks(DATA, 3) == EXPECTATION


def test_calculate_equal_interval_breaks():
    DATA = [0, 1, 1, 1, 3, 60, 3, 6]
    EXPECTATION = [0, 20.0, 40.0]
    assert calculate_equal_interval_breaks(DATA, 3) == EXPECTATION
