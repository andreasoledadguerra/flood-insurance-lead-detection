import numpy as np
from typing import Tuple
import rasterio
from rasterio.transform import from_bounds


from constants import CRS_32721
class SpatialGrid:

    @staticmethod   
    def interpolate_grid(
            bounds: Tuple[float, float, float, float],
            step: int = 100
        ) -> Tuple[np.ndarray, np.ndarray]:

            # Crear malla con np.mgrid
            grid_x, grid_y = np.mgrid[bounds[0]:bounds[2]:step*1j, bounds[1]:bounds[3]:step*1j]

            # Crear coordenadas de la malla
            grid_coords = np.column_stack([grid_x.ravel(), grid_y.ravel()])

            return grid_x, grid_y, grid_coords

    @staticmethod
    def convert_to_2d_grid(
        data: Tuple[np.ndarray, np.ndarray], 
        grid_shape: Tuple[int, int]
    ) -> Tuple[np.ndarray, np.ndarray]:
        # Desempaquetar la tupla data
        z, ss = data 
        # Convertir a grillas 2D los valores predichos
        z_2d = z.reshape(grid_shape)
        # Convertir a grillas 2D las desviacciones estándar(incertidumbre)
        ss_2d = ss.reshape(grid_shape)
        return z_2d, ss_2d
    
    @staticmethod
    def write_geotiff(grid_array: np.ndarray, 
                  bounds_proj: np.ndarray, 
                  filename: str, 
                  crs_epsg= CRS_32721) -> str:
        # Obtener dimensiones del array
        height, width = grid_array.shape
        # Calcular la transformación georreferenciada
        transform = from_bounds(bounds_proj[0], bounds_proj[1], 
                              bounds_proj[2], bounds_proj[3], 
                              width, height)
        with rasterio.open(
            filename,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=grid_array.dtype,
            #crs=CRS_32721.from_epsg(crs_epsg),
            crs=crs_epsg,
            transform=transform,
            compress='lzw'
        ) as dst:
            dst.write(grid_array, 1)
        return filename