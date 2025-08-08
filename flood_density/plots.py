import geopandas as gpd


CRS_4326 = 4326


def convert_kml_to_geojson(kml_file: str, output_file: str) -> str:
    gdf = gpd.read_file(kml_file, driver="KML")
    gdf.to_file(output_file, driver='GeoJSON')
    gdf.plot()
    
    return output_file


def export_to_geojson(gdf: gpd.GeoDataFrame, output_path: str) -> str:
    gdf.to_file(output_path, driver='GeoJSON')

    return output_path



