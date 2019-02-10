"""Example of a LIDAR point cloud, plotted using the PointCloudLayer.

Plots over 1.6M points.
"""
import slayer as sly
import pandas as pd


URL = 'https://raw.githubusercontent.com/ajduberstein/oakland_point_cloud/master/%s'
DATA_URL = URL % 'lidar_chunks_1.csv'
DATA_URL_2 = URL % 'lidar_chunks_2.csv'
LOOKUP_URL = URL % 'ground_truth_label.csv'
lidar = pd.concat([pd.read_csv(DATA_URL), pd.read_csv(DATA_URL_2)])
lookup = pd.read_csv(LOOKUP_URL)
lidar = lidar.merge(lookup)

v = sly.OrbitView()

color_scale = sly.ColorScale(
    palette='random',
    variable_name='label_name',
    scale_type='categorical_random')

s = sly.Slayer(v, add_legend=False, blend=True) + \
    sly.PointCloudLayer(
        lidar[['x', 'y', 'z', 'label_name']],
        position=['x', 'y', 'z'],
        color=color_scale,
        radius_pixels=15)
s.to_html('point_cloud.html', interactive=True)
