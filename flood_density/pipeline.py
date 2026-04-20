from dataclasses import dataclass
import numpy as np
from geopandas import GeoDataFrame
from sklearn.gaussian_process import GaussianProcessRegressor

from flood_density.preprocess import (
    clip_density_to_urban_area,
    extract_coords_from_geometry,
    extract_centroids_from_gdf,
    interpolate_grid,
    fit_gpr_model,
    convert_to_2d_grid,
)

@dataclass
class UrbanFloodData:
    casco_urbano: GeoDataFrame
    coordinates: np.ndarray
    centroids: np.ndarray
    bounds: np.ndarray
    grid_x: np.ndarray
    grid_y: np.ndarray
    gris_coords: np.ndarray
    gpr_fit: GaussianProcessRegressor
    grid_2d: np.ndarray

def build_urban_area(
    gdf_coordinates: GeoDataFrame,
    gdf_peligrosidad: GeoDataFrame,
    casco_urbano_utm: GeoDataFrame,
)-> tuple[GeoDataFrame, np.ndarray, np.ndarray]:
    """Etapa 1: recorte y extracción de geometría urbana."""
    casco_urbano = clip_density_to_urban_area(gdf_coordinates, gdf_peligrosidad)
    coordinates = extract_coords_from_geometry(casco_urbano_utm)
    centroids = extract_centroids_from_gdf(casco_urbano_utm, "Z")
    return casco_urbano, coordinates, centroids

def build_interpolation_grid(
    gdf_polygon: GeoDataFrame,
    step: int = 100,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Etapa 2: construcción de la grilla de interpolación."""
    bounds = gdf_polygon.total_bounds
    grid_x, grid_y, grid_coords = interpolate_grid(bounds, step=step)
    return grid_x, grid_y, grid_coords

def fit_and_predict(
    gpr_model: GaussianProcessRegressor,
    coordinates: np.ndarray,
    centroids: np.ndarray,
    predict_grid: np.ndarray,
    grid_shape: tuple,
) -> tuple[GaussianProcessRegressor, np.ndarray]:
    """Etapa 3: ajuste del modelo GPR y conversión a grilla 2D."""
    gpr_fit = fit_gpr_model(gpr_model, coordinates, centroids)
    grid_2d = convert_to_2d_grid(predict_grid, grid_shape)
    return gpr_fit, grid_2d

def run_flood_pipeline(
    gdf_coordinates: GeoDataFrame,
    gdf_peligrosidad: GeoDataFrame,
    casco_urbano_utm: GeoDataFrame,
    gdf_polygon: GeoDataFrame,
    gpr_model: GaussianProcessRegressor,
    predict_grid: np.ndarray,
    grid_step: int = 100,
) -> UrbanFloodData:
    """
    Orquesta el pipeline completo y devuelve un dataclass con todos
    los artefactos listos para graficar o consumir desde la UI.
    """
    casco_urbano, coordinates, centroids = build_urban_area(
        gdf_coordinates, gdf_peligrosidad, casco_urbano_utm
    )

    grid_x, grid_y, grid_coords = build_interpolation_grid(gdf_polygon, step=grid_step)

    gpr_fit, grid_2d = fit_and_predict(
        gpr_model, coordinates, centroids, predict_grid, grid_x.shape
    )

    return UrbanFloodData(
        casco_urbano=casco_urbano,
        coordinates=coordinates,
        centroids=centroids,
        bounds=gdf_polygon.total_bounds,
        grid_x=grid_x,
        grid_y=grid_y,
        grid_coords=grid_coords,
        gpr_fit=gpr_fit,
        grid_2d=grid_2d,
    )