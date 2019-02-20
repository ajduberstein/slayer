"""
Example of how to make a Scatterplot with a time component
"""
import slayer as sly
import pandas as pd


DATA_URL = 'https://raw.githubusercontent.com/ajduberstein/sf_growth/master/public/data/business.csv'
businesses = pd.read_csv(DATA_URL)

FUCHSIA_RGBA = [255, 0, 255, 140]

color_scale = sly.ColorScale(
    palette='random',
    variable_name='neighborhood',
    scale_type='categorical_random')

s = sly.Slayer(sly.Viewport(longitude=-122.43, latitude=37.76, zoom=11)) +\
    sly.Timer(tick_rate=0.75) + \
    sly.Scatterplot(
        businesses,
        position=['lng', 'lat'],
        color=color_scale,
        radius=50,
        time_field='start_date')
s.to_html('scatterplot.html', interactive=True)
