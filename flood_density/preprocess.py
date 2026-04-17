
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

CRS_4326 = 4326
CRS_32721 = 32721

class PreProcessData:
    
    def __init__(self, df: pd.DataFrame):
        self.df = df


    def convert_kml_to_gdf(kml_file: str) -> gpd.GeoDataFrame:
        gdf = gpd.read_file(kml_file, driver="KML")
        return gdf

    def export_to_geojson(gdf: gpd.GeoDataFrame, output_path: str) -> gpd.GeoDataFrame:
        gdf.to_file(output_path, driver='GeoJSON')
        return gdf

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

    def extract_centroids_from_gdf(gdf: gpd.GeoDataFrame, column_name: str) -> np.ndarray:

        # Extraer valores de una columna específica
        values = gdf[column_name].values
        print(f"Rango de valores: {values.min():.2f} - {values.max():.2f}")

        return values


    def extract_coords_from_geometry(gdf: gpd.GeoDataFrame) -> np.ndarray:

        # Extraer centroides y convertir a un array de coordenadas
        centroids = np.array([[point.x, point.y] for point in gdf.geometry.centroid])

        return centroids


   


    # Generar el modelo GaussianProcessRegressor
    def create_gpr_model(kernel: Kernel) -> GaussianProcessRegressor:
        gpr = GaussianProcessRegressor(kernel=kernel, alpha=1e-6, n_restarts_optimizer=10)
        return gpr

    # Ajustar el modelo GPR a los datos
    def fit_gpr_model(
        gpr: GaussianProcessRegressor, coords: np.ndarray, values: np.ndarray) -> GaussianProcessRegressor:

        gpr.fit(coords, values)
        return gpr


    def interpolate_grid(
        bounds: Tuple[float, float, float, float],
        step: int = 100
    ) -> Tuple[np.ndarray, np.ndarray]:

        # Crear malla con np.mgrid
        grid_x, grid_y = np.mgrid[bounds[0]:bounds[2]:step*1j, bounds[1]:bounds[3]:step*1j]

        # Crear coordenadas de la malla
        grid_coords = np.column_stack([grid_x.ravel(), grid_y.ravel()])

        return grid_x, grid_y, grid_coords

    def predict_grid(
        model: GaussianProcessRegressor, 
        grid: Tuple[np.ndarray, np.ndarray, np.ndarray]
    ) -> Tuple[np.ndarray, np.ndarray]:

        # Desempaquetar la tupla grid
        grid_x, grid_y, _ = grid

        # Preparar puntos para predicción
        points = np.column_stack((grid_x.ravel(), grid_y.ravel()))

        # Predecir
        z, ss = model.predict(points, return_std=True)

        return z, ss

    def convert_to_2d_grid(
        data: Tuple[np.ndarray, np.ndarray], 
        grid_shape: Tuple[int, int]
    ) -> Tuple[np.ndarray, np.ndarray]:

        # Desempaquetar la tupla data
        z, ss = data 

        # Convertir a grillas 2D los valores predichos
        z_2d = z.reshape(grid_shape)

        # Convertir a grillas 2D las desviacciones estándar(incertidumbre)
        ss_2d = ss.reshape(grid_shape)

        return z_2d, ss_2d


    def prepare_geospatial_bounds(gdf: gpd.GeoDataFrame) -> np.ndarray:

        # Obtener límites en coordenadas proyectadas
        bounds_proj = gdf.total_bounds  # [xmin, ymin, xmax, ymax]
        return bounds_proj

    def write_geotiff(grid_array: np.ndarray, 
                      bounds_proj: np.ndarray, 
                      filename: str, 
                      crs_epsg= CRS_32721) -> str:
        # Obtener dimensiones del array
        height, width = grid_array.shape

        # Calcular la transformación georreferenciada
        transform = from_bounds(bounds_proj[0], bounds_proj[1], 
                              bounds_proj[2], bounds_proj[3], 
                              width, height)

        with rasterio.open(
            filename,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=grid_array.dtype,
            crs=CRS.from_epsg(crs_epsg),
            transform=transform,
            compress='lzw'
        ) as dst:
            dst.write(grid_array, 1)

        return filename

    def run_kriging_pipeline(
        grid_2d_lp: np.ndarray, 
        gdf_la_plata_from_polygon: gpd.GeoDataFrame, 
        step: int = 100
    ) -> str:

        grid_lp = extract_grid_from_tuple(grid_2d_lp)
        geo_bounds_lp = prepare_geospatial_bounds(gdf_la_plata_from_polygon)
        geotiff_file = write_geotiff(
            grid_lp, 
            geo_bounds_lp, 
            'kriging_densidad_poblacional.tif', 
            32721
        )
        return geotiff_file