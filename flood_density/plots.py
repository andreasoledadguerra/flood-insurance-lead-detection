import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

from typing import List

CRS_4326 = 4326

def plot_gdf(gdf: gpd.GeoDataFrame):
    return gdf.plot()

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

def plot_kriging_results_with_basemap(gdf: gpd.GeoDataFrame, 
                                      coords: np.ndarray, 
                                      values: np.ndarray,
                                      bounds: Tuple[float, float, float, float], 
                                      grid_x: np.ndarray, 
                                      grid_y: np.ndarray, 
                                      model: OrdinaryKriging, 
                                      kriging_result: Tuple[object, np.ndarray]) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(10, 10))

    # Obtener la superficie interpolada desde la función predict_fn
    grid_z, ss = kriging_result
    
    # Plotear superficie Kriging interpolada
    contour = ax.contourf(grid_x, grid_y, grid_z, levels=30, cmap='viridis', alpha=0.5)
    

    # Plotear los polígonos originales
    casco_urbano_utm.plot(column='Z', 
               cmap='viridis',
               alpha=0.5,
               edgecolor='black',
               linewidth=1.0,
               ax=ax)

    # Plotear los polígonos originales con bordes
    casco_urbano_utm.plot(column='Z', 
               cmap='viridis',
               alpha=0.5,
               edgecolor='black',
               linewidth=1.0,
               ax=ax)

    # Plotear los puntos centroides
    scatter = ax.scatter(coords[:, 0], coords[:, 1],
                    c=gdf['Z'],
                    cmap='viridis',
                    s=30,
                    edgecolors='black',
                    linewidths=1,
                    zorder=5)

    # Ajustar límites del gráfico según los límites de La Plata
    ax.set_xlim(bounds[0], bounds[2])
    ax.set_ylim(bounds[1], bounds[3])

    #Mapa base más sutil
    ctx.add_basemap(ax, crs=casco_urbano_utm.crs.to_string(),
                   source=ctx.providers.CartoDB.Positron,
                   alpha = 0.9)

    # Agregar colorbar para el scatter
    plt.colorbar(scatter, ax=ax, label='Densidad poblacional',shrink=0.7, aspect=25)

    # Agregar título y etiquetas
    ax.set_title('Interpolación Kriging - Densidad Poblacional La Plata')
    ax.set_xlabel('X (UTM)')
    ax.set_ylabel('Y (UTM)')

    plt.tight_layout()
    plt.show()