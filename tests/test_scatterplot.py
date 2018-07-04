# -*- coding: utf-8 -*-

"""
Test Scatterplot
------------
"""
import os

import pandas as pd

from slayer import Slayer, layers, Viewport


data = pd.read_csv(os.path.join(os.path.dirname(__file__), './fixtures/cities.csv'))


def test_scatterplot():
    s = Slayer(Viewport(latitude=37.78, longitude=-122.45, zoom=13, bearing=10))
    layers.Scatterplot(data, latitude_field='lat', longitude_field='lng').add_to(s)
    EXPECTED = '''
      const layers = [
        new ScatterplotLayer({
            data: [{"lat":37.6957743533,"lng":-122.5394439697,"city":"SF"},{"lat":37.8265990579,"lng":-122.2874450684,"city":"SF"},{"lat":36.0382725592,"lng":-115.1940536499,"city":"Las Vegas"},{"lat":33.408516828,"lng":-112.1319580078,"city":"Phoenix"},{"lat":18.9634415956,"lng":-99.1845703125,"city":"Ciudad de Mexico"},{"lat":41.5820659886,"lng":-88.1597900391,"city":"Chicago"},{"lat":40.7259253407,"lng":-73.999786377,"city":"New York"}],
            getColor: function (x) { return x["color"] || [0, 0, 0] },
            getPosition: function (x) { return [x["lng"], x["lat"]] },
            getRadius: function (x) { return x["radius"] || 100 }})
      ];'''
    assert EXPECTED.replace(' ', '') in s.to_html().replace(' ', '')
