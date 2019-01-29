slayer.py 
================

.. image:: https://travis-ci.com/ajduberstein/slayer.svg?branch=master
    :target: https://travis-ci.com/ajduberstein/slayer


Short for "Spatial Layers," `Slayer` is a Python wrapper around `deck.gl`_.

.. _deck.gl: http://deck.gl/#/

Example usage
================

Plotting all registered businesses in San Francisco by neighborhood:

.. code-block:: python
>>> import slayer as sly
>>> import pandas as pd
>>> DATA_URL = 'https://raw.githubusercontent.com/ajduberstein/sf_growth/master/public/data/business.csv'
>>> # A data frame of all the businesses registered in SF in the last 50+ years
>>> businesses = pd.read_csv(DATA_URL).fillna(0)
>>> # Automatically fit to the center 95% of your data
>>> auto_view = sly.Viewport.autocompute(businesses[['lng', 'lat']], view_proportion=0.95)
>>> # Create a random set of 100 colors, on the variable `neighborhood`
>>> color_scale = sly.ColorScale(
... num_classes=100,
... palette='random',
... variable_name='neighborhood',
... scale_type='categorical_random')
>>> # Create a geospatial scatterplot
>>> s = sly.Slayer(auto_view, drag_boxes=True)
>>> L = sly.Scatterplot(
... businesses,
... position=['lng', 'lat'],
... radius=50,
... color=color_scale)
>>> # Write it out to disk and visualize it
>>> # If in a Jupyter notebook, a pane will open
>>> (s + L).to_html('demo.html', interactive=True)

Installation
===========

Get a `Mapbox API key`_ and set it as an environment variable (or list it in your script as above).

.. _Mapbox API key: https://www.mapbox.com/help/how-access-tokens-work/#mapbox-tokens-api

This isn't on pip yet.

In the shell, go:

.. code-block:: python
>>> git clone https://github.com/ajduberstein/slayer
>>> python setup.py install
