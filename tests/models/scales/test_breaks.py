# -*- coding: utf-8 -*-
"""
Test Data Break Calculations
------------
"""
from slayer.models.scales.breaks import (
    calculate_percentile_breaks,
    calculate_equal_interval_breaks,
)


def test_calculate_percentile_breaks():
    DATA = [0, 1, 1, 1, 3, 60, 3, 6]
    EXPECTATION = [0, 1.0, 3.0]
    assert calculate_percentile_breaks(DATA, 3) == EXPECTATION


def test_calculate_equal_interval_breaks():
    DATA = [0, 1, 1, 1, 3, 60, 3, 6]
    EXPECTATION = [0, 20.0, 40.0]
    assert calculate_equal_interval_breaks(DATA, 3) == EXPECTATION
