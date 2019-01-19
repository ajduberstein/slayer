slayer.py 
================

.. image:: https://travis-ci.com/ajduberstein/slayer.svg?branch=master
    :target: https://travis-ci.com/ajduberstein/slayer


Short for "Spatial Layers," `Slayer` is a Python wrapper around `deck.gl`_.

.. _deck.gl: http://deck.gl/#/

Example usage
================

Get a `Mapbox API key`_ and set it as an environment variable (or list it in your script as below):

For example, to plot 1 million points with a red-to-purple color scale, you can do the following:

.. _Mapbox API key: https://www.mapbox.com/help/how-access-tokens-work/#mapbox-tokens-api

.. code-block:: python
>>> import slayer as sly
>>> from random import uniform
>>> data = [{
...     'lat': 200*uniform(-1, 1),
...     'lng': 200*uniform(-1, 1),
>>> } for x in range(0, 1000000)]
>>> s = sly.Slayer(sly.Viewport(0, 0, zoom=5), mapbox_api_key='pk.YOUR_API_KEY') +\
...     sly.Scatterplot(data, color=sly.ColorScale('lat', 'RdPu'))
>>> s.to_html(interactive=True)

Installation
===========

Clone this directory and run code`python setup.py install` and `cd examples` in this folder and have a look around.
