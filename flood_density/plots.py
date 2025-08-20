import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt


from typing import List

CRS_4326 = 4326

#def convert_kml_to_gdf(kml_file: str) -> gpd.GeoDataFrame:
    #gdf = gpd.read_file(kml_file, driver="KML")
    #return gdf

#def export_to_geojson(gdf: gpd.GeoDataFrame, output_path: str) -> str:
    #geojson = gdf.to_file(output_path, driver='GeoJSON')

    #return geojson

#def plot_gdf(gdf: gpd.GeoDataFrame, str : "La Plata Geospatial Data") -> None:
    
    #return gdf.plot()


def city_bounds_and_density_plot(gdf: gpd.GeoDataFrame, centroides: np.ndarray, values_density: np.ndarray, bound: List[float]) -> plt.Figure:
    
    fig, ax = plt.subplots(figsize=(12, 10))

    # Plot del polígono
    gdf.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2, alpha=0.8)

    # Plot de los puntos de densidad
    sc = ax.scatter(
        centroides[:,0], centroides[:,1],
        c=values_density,
        cmap='viridis', s=100,
        edgecolor='black', linewidths=1, alpha=0.9
    )

    minx, miny, maxx, maxy = bound
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    # Colorbar
    plt.colorbar(sc, ax=ax, label="Densidad Poblacional", shrink=0.9)

    # Título
    ax.set_title('Densidad en contexto del Casco Urbano de La Plata', fontsize=16)

    return plt.show()

