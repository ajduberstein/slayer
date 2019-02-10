slayer.py 
================

[![build](https://travis-ci.com/ajduberstein/slayer.svg?branch=master)](https://travis-ci.com/ajduberstein/slayer)

![alt text](https://camo.githubusercontent.com/5da3ed41336cdccc6f186d13e9de7e97cced98b3/687474703a2f2f692e696d6775722e636f6d2f6d7666766766302e6a7067 "slayer.py")

Short for "Spatial Layers," Slayer is a Python wrapper around [deck.gl](http://deck.gl/#/).

_Features_

- Scale. Built on WebGL, Slayer plots hundreds of thousands of points.
- Focus on Data Science, Analytics, and GIS. API treats Pandas as a first class citizen.
- Time. Built for plotting data over time.

For example, 1.6M LIDAR points visualized here:

![slayer.py](https://media.giphy.com/media/YlI1IGJHaNw1We9se7/giphy.gif)

Example usage
================

Plotting all registered businesses in San Francisco by neighborhood:

```python
import slayer as sly
import pandas as pd

# A data frame of all the businesses registered in SF in the last 50+ years
DATA_URL = 'https://raw.githubusercontent.com/ajduberstein/sf_growth/master/public/data/business.csv'
businesses = pd.read_csv(DATA_URL)

# Automatically fit to the center 95% of your data
auto_view = sly.Viewport.autocompute(businesses[['lng', 'lat']], view_proportion=0.95)

# Create a random set of 100 colors, on the variable `neighborhood`
color_scale = sly.ColorScale(
   num_classes=100,
   palette='random',
   variable_name='neighborhood',
   scale_type='categorical_random')

# Create a geospatial scatterplot
s = sly.Slayer(auto_view, drag_boxes=True)
L = sly.Scatterplot(
   businesses,
   position=['lng', 'lat'],
   radius=50,
   color=color_scale)

# Write it out to disk and visualize it
# If in a Jupyter notebook, a pane will open
(s + L).to_html('demo.html', interactive=True)
```

Installation
===========

Get a [Mapbox API key](https://www.mapbox.com/help/how-access-tokens-work/#mapbox-tokens-api) and
set it as an environment variable (or list it in your script as above).

This package isn't on Pip yet.

In the shell, type:

```bash
>>> git clone https://github.com/ajduberstein/slayer
>>> cd slayer
>>> python setup.py install
```
