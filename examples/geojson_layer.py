import slayer as sly
import requests as r
from slayer.io import geojson_to_df

DATA_URL = 'https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/geojson/vancouver-blocks.json'
response = r.get(DATA_URL)
json = response.json()
data = geojson_to_df(json)
s = sly.Slayer(sly.Viewport(latitude=49.2576508, longitude=-123.2639868, zoom=11))
# TODO make this geojson into a polygon
g = sly.PolygonLayer()
(s + g).to_html('geojson.html', interactive=True)
