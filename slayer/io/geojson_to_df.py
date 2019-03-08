from pandas.io.json import json_normalize
import pandas as pd

def geojson_to_pandas_df(geojson):
    """Converts geojson to a pandas dataframe

    Credit to https://stackoverflow.com/questions/47113449/convert-geo-json-with-nested-lists-to-pandas-dataframe

    Args:
        geojson (dict): GeoJSON as a dictionary

    Returns:
        pandas.DataFrame: Flattened version of GeoJSON input

    """
    df = json_normalize(geojson['features'])
    coords = 'geometry.coordinates'
    flattened_df = df[coords]\
        .apply(lambda r: [(i[0], i[1]) for i in r[0]])\
        .apply(pd.Series).stack().reset_index(level=1)\
        .rename(columns={0: coords, 'level_1': 'point'})\
        .join(df.drop(coords, 1), how='left').reset_index(level=0)
    flattened_df[['lng', 'lat']] = flattened_df[coords].apply(pd.Series)
    return flattened_df
