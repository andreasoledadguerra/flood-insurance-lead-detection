import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from typing import Dict


def extract_city_bounds_from_dataframe_to_geodataframe(df: pd.DataFrame, lat_col: str, lon_col: str) -> gpd.GeoDataFrame:

    geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df.copy(), geometry=geometry, crs="EPSG:4326")

    return gdf


def extract_city_bounds(df: pd.DataFrame) -> Dict[str, float]:    
# Extraer límites
    minx, miny = df['longitude'].min(), df['latitude'].min()
    maxx, maxy = df['longitude'].max(), df['latitude'].max()

    return {
        "x_min": minx,
        "y_min": miny,
        "x_max": maxx,
        "y_max": maxy
    }
