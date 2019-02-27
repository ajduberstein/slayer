import slayer as sly
import requests as r

#make_js_get_elevation_value Grab the data
DATA_URL = 'https://raw.githubusercontent.com/uber-common/deck.gl-data/master/examples/geojson/vancouver-blocks.json'
response = r.get(DATA_URL)
json = response.json()
s = sly.Slayer(sly.Viewport(longitude=49.2576508, latitude=-123.2639868, zoom=11))
g = sly.GeoJsonLayer(json)
(s + g).to_html('geojson.html', interactive=True)
