import pandas as pd
import geopandas as gpd
import numpy as np


from shapely.geometry import box, Point, Polygon
from typing import Dict, List, Tuple
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel


CRS_4326 = 4326


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

def extract_bounds_polygon(coordinates: Dict[str, float]) -> Polygon:
    
    return Polygon([
        (coordinates["x_min"], coordinates["y_min"]),   # SW (suroeste)
        (coordinates["x_max"], coordinates["y_min"]),   # SE (sureste)  
        (coordinates["x_max"], coordinates["y_max"]),   # NE (noreste)
        (coordinates["x_min"], coordinates["y_max"]),   # NW (noroeste)
        (coordinates["x_min"], coordinates["y_min"])    # Cerrar polígono
    ])


# Convertir el polígono en un geodataframe
def polygon_to_gdf(polygon: Polygon, crs= CRS_4326) -> gpd.GeoDataFrame:

    return gpd.GeoDataFrame(
        geometry=[polygon],
        crs=crs  # CRS WGS 84
    )


def gdf_to_geojson(gdf: gpd.GeoDataFrame) -> str:
    return gdf.to_json()


#Function that convert dictionary of coordinates in polygon
def coordinates_to_box(coord : dict)-> Polygon:

    return box(
        coord['x_min'],
        coord['y_min'],
        coord['x_max'],
        coord['y_max'],
    )

def points_geocoordinates(df: pd.DataFrame) -> Polygon:
    # Crear geometría de puntos usando X,Y como longitud,latitud
    geometry = [Point(xy) for xy in zip(df['X'], df['Y'])]

    return Polygon(geometry)

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

def prepare_coords(gdf: gpd.GeoDataFrame, value_column: str) -> np.ndarray:

    # Extraer valores de una columna específica
    values = gdf[value_column].values
    print(f"Rango de valores: {values.min():.2f} - {values.max():.2f}")
    
    return values


def prepare_centroids(gdf: gpd.GeoDataFrame) -> np.ndarray:

    # Extraer centroides y convertir a un array de coordenadas
    centroids = np.array([[point.x, point.y] for point in gdf.geometry.centroid])
    
    return centroids


# Función para crear un kernel de Kriging
def create_kriging_kernel(constant_value=1.0, length_scale=1000.0, noise_level=0.1,
                         length_scale_bounds=(1e-5, 1e5), noise_level_bounds=(1e-10, 1e3)):
    """
    Crea un kernel para un modelo de Kriging (Gaussian Process).
    
    El kernel resultante tiene la forma: C * RBF + WhiteKernel
    donde C es una constante, RBF es el kernel de función de base radial,
    y WhiteKernel modela el ruido en las observaciones.
    
    Parámetros:
    -----------
    constant_value : float, default=1.0
        Valor inicial del ConstantKernel (amplitud del proceso)
    length_scale : float, default=1000.0
        Valor inicial del RBF kernel (escala de correlación espacial)
    noise_level : float, default=0.1
        Valor inicial del WhiteKernel (nivel de ruido)
    length_scale_bounds : tuple, default=(1e-5, 1e5)
        Límites para optimización del parámetro length_scale del RBF
    noise_level_bounds : tuple, default=(1e-10, 1e3)
        Límites para optimización del parámetro noise_level del WhiteKernel
    
    Returns:
    --------
    kernel : sklearn.gaussian_process.kernels.Kernel
        Objeto kernel listo para usar en GaussianProcessRegressor
    
    """
    
    # Kernel constante (amplitud)
    constant_kernel = ConstantKernel(constant_value, constant_value_bounds="fixed")
    
    # Kernel RBF (correlación espacial)
    rbf_kernel = RBF(length_scale=length_scale, length_scale_bounds=length_scale_bounds)
    
    # Kernel de ruido
    noise_kernel = WhiteKernel(noise_level=noise_level, noise_level_bounds=noise_level_bounds)
    
    # Combinar kernels: (Constante * RBF) + Ruido
    kernel = constant_kernel * rbf_kernel + noise_kernel
    
    return kernel


# Generar el modelo GaussianProcessRegressor
def create_gpr_model(kernel= kernel) -> GaussianProcessRegressor:
    gpr = GaussianProcessRegressor(kernel=kernel, alpha=1e-6, n_restarts_optimizer=10)
    return gpr