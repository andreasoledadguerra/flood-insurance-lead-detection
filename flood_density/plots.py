import geopandas as gpd


CRS_4326 = 4326


def convert_kml_to_geojson(kml_file: str, output_file: str) -> None:
    gdf = gpd.read_file(kml_file, driver="KML")
    gdf.to_file(output_file, driver='GeoJSON')
    gdf.plot()

    print(f"Converted {kml_file} to {output_file}") 
    
    return output_file



def export_to_geojson(gdf: gpd.GeoDataFrame, output_path) -> str:
    gdf.to_file(output_path, driver='GeoJSON')
    print(f"Archivo exportado: {output_path}")

    return output_path
