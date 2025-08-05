import pandas as pd
import geopandas as gpd
from shapely.geometry import Point,Polygon
from typing import Dict

CRS_4326 = 4326

def extract_city_bounds(gdf: gpd.GeoDataFrame) -> Dict[str,float]:
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

def extract_city_bounds_from_dataframe_to_geodataframe(df: pd.DataFrame, lat_col: str, lon_col: str) -> gpd.GeoDataFrame:

    geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df.copy(), geometry=geometry, crs="EPSG:4326")

    return gdf
