import numpy as np
from typing import Tuple

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