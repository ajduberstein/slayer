slayer.py
================

`Slayer` is a Python wrapper around `deck.gl`_.

.. _deck.gl: http://deck.gl/#/

Example usage
================

Get a `Mapbox API key`_ and set it as an environment variable (or list it in your script as below):

For example, to plot 1 million points with a red-to-purple color scale, you can do the following:

.. _Mapbox API key: https://www.mapbox.com/help/how-access-tokens-work/#mapbox-tokens-api

.. code-block:: python
>>> from random import random
>>> data = [{
...     'lat': 100*random(),
...     'lng': 100*random(),
>>> } for x in range(0, 1000000)]
>>> s = sly.Slayer(sly.Viewport(0, 0, zoom=5), mapbox_api_key='pk.YOUR_API_KEY') +\
...     sly.Scatterplot(data, color=sly.ColorScale('lat', 'RdPu'))
>>> s.to_html(interactive=True)
