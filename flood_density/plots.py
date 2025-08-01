def convert_kml_to_geojson(kml_file: str, output_file: str) -> None:
    """
    Convert a KML file to GeoJSON format.
    
    Parameters:
    kml_file (str): Path to the input KML file.
    output_file (str): Path to save the output GeoJSON file.
    """
    gdf = gpd.read_file(kml_file, driver="KML")
    gdf.to_file(output_file, driver='GeoJSON')
    gdf.plot()

    print(f"Converted {kml_file} to {output_file}") 
    
    return output_file

 pass
