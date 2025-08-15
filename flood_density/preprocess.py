import pandas as pd
import geopandas as gpd
from shapely.geometry import box, Point, Polygon
from typing import Dict, List, Tuple

CRS_4326 = 4326

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
def extract_city_data(df: pd.DataFrame, city_name: str, bounds_dict: dict) -> pd.DataFrame:

    # Filter data based on city boundaries
    city_data = df[
        (df['X'] >= bounds_dict['x_min']) & 
        (df['X'] <= bounds_dict['x_max']) & 
        (df['Y'] >= bounds_dict['y_min']) & 
        (df['Y'] <= bounds_dict['y_max'])
    ]
    
    # Save filtered data to CSV file
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
def polygon_to_geodataframe(polygon: Polygon, crs: CRS_4326) -> gpd.GeoDataFrame:

    return gpd.GeoDataFrame(
        geometry=[polygon],
        crs=crs  # CRS WGS 84
    )


def convert_gdf_to_geojson(gdf: gpd.GeoDataFrame, output_file: str) -> None:
    gdf.to_file(output_file, driver='GeoJSON')
    gdf.plot()

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

    return geometry

def convert_points_in_gdf(points_list: List[Point], crs=CRS_4326) -> gpd.GeoDataFrame:
        gdf= gpd.GeoDataFrame(geometry= points_list, crs=crs)
        return gdf


def extract_city_bounds_from_df_to_gdf(df: pd.DataFrame, lat_col: str, lon_col: str) -> gpd.GeoDataFrame:

    geometry = [Point(lon, lat) for lon, lat in zip(df[lon_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df.copy(), geometry=geometry, crs="EPSG:4326")

    return gdf
