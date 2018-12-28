slayer.py
================

`Slayer` is a Python wrapper around `deck.gl`_.

.. _deck.gl: http://deck.gl/#/

Example usage
================

Get a `Mapbox API key`_ and set it as an environment variable (or list it in your script as below):

.. _Mapbox API key: https://www.mapbox.com/help/how-access-tokens-work/#mapbox-tokens-api

.. code-block:: python
>>> import slayer as sly
>>> # Plot 1 million points, to prove we can
>>> data = [{
...     'lat': 1.1 + x,
...     'lng': 0.2 + x,
...     'radius': 100000,
...     'color': [255, 165, 0]
>>> } for x in range(0, 1000000)]
>>> s = sly.Slayer(sly.Viewport(0, 0, zoom=5), mapbox_api_key='pk.YOUR_API_KEY') + sly.layers.Scatterplot(data)
>>> s.to_html()


.. code:: python
>>> import slayer as sly
>>> # Plot 1 million points, to prove we can
>>> data = pd.DataFrame([{
...     'lat': 1.1 + x,
...     'lng': 0.2 + x,
...     'radius': 100000,
... } for x in range(0, 1000000)])
# TODO start from here
>>> setColor(data['color'])
>>> s = sly.Slayer(sly.Viewport(0, 0, zoom=5), mapbox_api_key='pk.YOUR_API_KEY') + sly.layers.Scatterplot(data)
>>> s.to_html()
