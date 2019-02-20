"""
Example of how to make a HexagonLayer with a time component
"""
import slayer as sly
import pandas as pd

DATA_URL = 'https://raw.githubusercontent.com/ajduberstein/sf_growth/master/public/data/business.csv'
businesses = pd.read_csv(DATA_URL)
businesses['start_date'] = businesses['start_date'].apply(lambda x: str(x))

s = sly.Slayer(sly.Viewport(longitude=-122.43, latitude=37.76, zoom=12, bearing=-65, pitch=60)) + \
    sly.Timer(
        input_type='iso8601',
        tick_rate=0.5,
        increment_by='365 days',
        js_display_format='YYYY') + \
    sly.HexagonLayer(
        businesses.sample(n=20000),
        elevation_scale=1000,
        color_range='Blues',
        position=['lng', 'lat'],
        radius=100,
        time_field='start_date')
s.to_html('hexagon.html', interactive=True)
