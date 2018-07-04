slayer.py
================


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



`Slayer` is a Python wrapper around [deck.gl](deck.gl) 

Slayer does what many other mapping libraries cannot. For example,

- Using interactivity to inform scripting
- Works on an airplane
- Painless export of SVGs
- Plotting millions of points for exploratory data analysis (or dramatic effect)
- Playing data over time

Name 
================

Slayer is short for __Spatial Layers__ and is also a manufacturer of espresso machine


Example usage
================

>>> DATA = [{'latitude': 1.1 + x, 'longitude': 0.2 + x, 'radius': 100000, 'color': [255, 165, 0]} for x in range(0, 1000000)]
>>> s = Slayer(Viewport(0, 0, zoom=10), mapbox_api_key='YOUR_API_KEY') + layers.Scatterplot(data)
>>> s.to_html(interactive=True)
