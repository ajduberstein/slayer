slayer.py
================

::

                        (
                          )     (
                   ___...(-------)-....___
               .-""       )    (          ""-.
         .-'``'|-._             )         _.-|
        /  .--.|   `""---...........---""`   |
       /  /    |                             |
       |  |    |                             |
        \  \   |                             |
         `\ `\ |      S L A Y E R . P Y      |
           `\ `|                             |
           _/ /\                             /
          (__/  \                           /
       _..---""` \                         /`""---.._
    .-'           \                       /          '-.
   :               `-.__             __.-'              :
   :                  ) ""---...---"" (                 :
    '._               `"--...___...--"`              _.'
      \""--..__                              __..--""/
       '._     """----.....______.....----"""     _.'
          `""--..,,_____            _____,,..--""`
                        `"""----"""`




`Slayer` is a Python wrapper around `deck.gl`_.

.. _deck.gl: http://deck.gl/#/

Example usage
================

.. code:: python
>>> data = [{'latitude': 1.1 + x, 'longitude': 0.2 + x, 'radius': 100000, 'color': [255, 165, 0]} for x in range(0, 1000000)]
>>> s = Slayer(Viewport(0, 0, zoom=10), mapbox_api_key='YOUR_API_KEY') + layers.Scatterplot(data)
>>> s.to_html(interactive=True)
