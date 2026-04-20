
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio

from rasterio.crs import CRS
from rasterio.transform import from_bounds

from shapely.geometry import box, Point, Polygon

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (
    ConstantKernel,
    Kernel,
    RBF,
    WhiteKernel,
)

from constants import CRS_32721,CRS_4326

class PreProcessData:
    
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_bounds_xy_min_max(gdf: gpd.GeoDataFrame) -> Dict[str,float]:
        # Extraer límites
        minx, miny, maxx, maxy = gdf.total_bounds
        return {
            "x_min": minx,
            "y_min": miny,
            "x_max": maxx,
            "y_max": maxy
        }


    # Function to extract data from a specific city in the complete dataset
    def extract_city_data(df: pd.DataFrame, city_name: str, bounds_dict: dict, with_save: bool = True) -> pd.DataFrame:

        # Filter data based on city boundaries
        city_data = df[
            (df['X'] >= bounds_dict['x_min']) & 
            (df['X'] <= bounds_dict['x_max']) & 
            (df['Y'] >= bounds_dict['y_min']) & 
            (df['Y'] <= bounds_dict['y_max'])
        ]

        # Save filtered data to CSV file
        if with_save:
            output_file = f"{city_name.lower().replace(' ', '_')}_population_2020.csv"
            city_data.to_csv(output_file, index=False)

        return city_data



    # Convertir el polígono en un geodataframe
    def polygon_to_gdf(polygon: Polygon, crs= CRS_4326) -> gpd.GeoDataFrame:

        return gpd.GeoDataFrame(
            geometry=[polygon],
            crs=crs  # CRS WGS 84
        )


    def gdf_to_geojson(gdf: gpd.GeoDataFrame) -> str:
        return gdf.to_json()


    def convert_points_in_gdf(points_list: List[Point], crs=CRS_4326) -> gpd.GeoDataFrame:
        gdf = gpd.GeoDataFrame(geometry=points_list, crs=crs)
        return gdf


    def extract_city_bounds_from_df_to_gdf(df: pd.DataFrame, lat_col: str, lon_col: str) -> gpd.GeoDataFrame:

        geometry = [Point(lon, lat) for lon, lat in zip(df[lon_col], df[lat_col])]
        gdf = gpd.GeoDataFrame(df.copy(), geometry=geometry, crs="EPSG:4326")

        return gdf

    def clip_density_to_urban_area(gdf_1: gpd.GeoDataFrame, gdf_2: gpd.GeoDataFrame) -> gpd.GeoDataFrame: 
        # Usar uniones espaciales para mantener solo puntos dentro del casco urbano
        points_in_casco = gpd.sjoin(gdf_1, gdf_2, how='inner', predicate='intersects')

        # Limpiar columnas duplicadas del join 
        points_in_casco = points_in_casco.drop(columns=[col for col in points_in_casco.columns if col.endswith('_right')]) 

        return points_in_casco
        

    def extract_coords_from_geometry(gdf: gpd.GeoDataFrame) -> np.ndarray:

        # Extraer centroides y convertir a un array de coordenadas
        centroids = np.array([[point.x, point.y] for point in gdf.geometry.centroid])

        return centroids




