import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from typing import Dict


def extract_city_bounds(df: pd.DataFrame) -> Dict[str, float]:    
# Extraer límites
    minx, miny = df['X'].min(), df['Y'].min()
    maxx, maxy = df['X'].max(), df['Y'].max()

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


def extract_city_bounds_from_dataframe_to_geodataframe(df: pd.DataFrame, lat_col: str, lon_col: str) -> gpd.GeoDataFrame:

    geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
    gdf = gpd.GeoDataFrame(df.copy(), geometry=geometry, crs="EPSG:4326")

    return gdf
