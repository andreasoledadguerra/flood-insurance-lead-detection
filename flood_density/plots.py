import geopandas as gpd


CRS_4326 = 4326


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


def export_to_geojson(gdf_densidad: gpd.GeoDataFrame, output_path:str = "la_plata_densidad.geojson") -> str:
        """
    Exporta un GeoDataFrame a formato GeoJSON
    
    Args:
        gdf_densidad: GeoDataFrame con datos de densidad
        output_path: Ruta de salida (default: "la_plata_densidad.geojson")
    
    Returns:
        str: Ruta del archivo exportado
    """
        
        gdf_densidad.to_file(output_path, driver='GeoJSON')
        print(f"Archivo exportado: {output_path}")

        return output_path

    pass