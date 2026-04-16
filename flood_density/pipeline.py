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

    