"""
Example of a LIDAR point cloud, plotted using the PointCloudLayer.
"""
import slayer as sly
import pandas as pd


DATA_URL = 'https://raw.githubusercontent.com/ajduberstein/oakland_point_cloud/master/lidar_chunks_1.csv'
DATA_URL_2 = 'https://raw.githubusercontent.com/ajduberstein/oakland_point_cloud/master/lidar_chunks_2.csv'
lidar = pd.concat([pd.read_csv(DATA_URL), pd.read_csv(DATA_URL_2)])

v = sly.OrbitView()

color_scale = sly.ColorScale(
    palette='random',
    variable_name='label_id',
    scale_type='categorical_random')

s = sly.Slayer(v) + \
    sly.PointCloudLayer(
        lidar,
        position=['x', 'y', 'z'],
        color=color_scale,
        radius_pixels=1000)
s.to_html('point_cloud.html', interactive=True)
