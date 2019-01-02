# -*- coding: utf-8 -*-

"""
Test Scatterplot
------------
"""
# import os
# 
# import pandas as pd
# 
# from slayer import Slayer, layers, Viewport
# 
# from .utils import check_js_equal
# 
# 
# data = pd.read_csv(os.path.join(os.path.dirname(__file__), './fixtures/cities.csv'))
# expected = open(os.path.join(os.path.dirname(__file__), './fixtures/expected/scatterplot.js'), 'r').read()
# 
# 
# def test_scatterplot():
#     s = Slayer(Viewport(latitude=37.78, longitude=-122.45, zoom=13, bearing=10))
#     layers.Scatterplot(data, position=['lng', 'lat']).add_to(s)
#     actual = s.to_html(js_only=True)
#     assert check_js_equal(expected, actual)
