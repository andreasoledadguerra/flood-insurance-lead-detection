    def convert_kml_to_gdf(kml_file: str) -> gpd.GeoDataFrame:
        gdf = gpd.read_file(kml_file, driver="KML")
        return gdf

    def export_to_geojson(gdf: gpd.GeoDataFrame, output_path: str) -> gpd.GeoDataFrame:
        gdf.to_file(output_path, driver='GeoJSON')
        return gdf