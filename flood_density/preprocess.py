import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from typing import Dict


def extract_city_bounds_from_dataframe_to_geodataframe(df: pd.DataFrame, lat_col: str, lon_col: str) -> gpd.GeoDataFrame:

    geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df.copy(), geometry=geometry, crs="EPSG:4326")

    return gdf


def extract_city_bounds(gdf: gpd.GeoDataFrame) -> Dict[str, float]:    
# Extraer límites
    minx, miny, maxx, maxy = gdf.total_bounds

    return {
        "west_longitude": minx,
        "south_latitude": miny,
        "east_longitude": maxx,
        "north_latitude": maxy
    }
