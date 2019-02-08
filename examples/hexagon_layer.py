"""
Example of how to make a HexagonLayer with a time component
"""
import slayer as sly
import pandas as pd

DATA_URL = 'https://raw.githubusercontent.com/ajduberstein/sf_growth/master/public/data/business.csv'
businesses = pd.read_csv(DATA_URL)


s = sly.Slayer(sly.Viewport(longitude=-122.43, latitude=37.76, zoom=11)) +\
    sly.HexagonLayer(
        businesses.sample(n=20000),
        elevation_scale=1000,
        color_range='OrRd',
        position=['lng', 'lat'],
        radius=100,
        time_field='start_date')
s.to_html('hexagon.html', interactive=True)
