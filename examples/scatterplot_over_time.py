import pandas as pd
import slayer as sly
"""
View 2014 Uber data from 538 played over time
"""


# Use 538's 2014 Uber data
uber_pickups = ('https://raw.githubusercontent.com/fivethirtyeight/uber-tlc-foil-response/'
                'master/uber-trip-data/uber-raw-data-apr14.csv')

df = pd.read_csv(uber_pickups)
df['Date/Time'] = df['Date/Time'].apply(lambda d: pd.Timestamp.strptime(d, '%m/%d/%Y %H:%M:%S'))


v = sly.Viewport.autocompute(df[['Lon', 'Lat']])
t = sly.Timer(input_type='datetime', increment_by='1 hour', tick_rate=0.5)
s = sly.Slayer(viewport=v, timer=t)
p = sly.Scatterplot(df, radius=100, position=['Lon', 'Lat'], time_field='Date/Time')
(s + p).to_html('scatterplot_over_time.html', interactive=True)
