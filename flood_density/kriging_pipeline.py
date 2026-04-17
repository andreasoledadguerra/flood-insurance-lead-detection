import numpy as np
import geopandas as gpd
from typing import Tuple
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (
    ConstantKernel,
    Kernel,
    RBF,
    WhiteKernel,
)

class KrigingModel:
    """ Encapsula el ciclo completo de Kriging: kernel -> modelo -> fit -> predicción -> grilla"""

    # -------------------------------------------------------------------------
    # 1. Construcción del kernel y modelo
    # -------------------------------------------------------------------------

    def create_kriging_kernel(
        constant_value: float =1.0, 
        length_scale: float =1000.0, 
        noise_level: float=0.1,
        length_scale_bounds: Tuple[float,float]=(1e-5, 1e5), 
        noise_level_bounds: Tuple[float, float]=(1e-10, 1e3),
        ) -> Kernel:
        """
        Crea un kernel para un modelo de Kriging (Gaussian Process).

        El kernel resultante tiene la forma: C * RBF + WhiteKernel
        donde C es una constante, RBF es el kernel de función de base radial,
        y WhiteKernel modela el ruido en las observaciones.

        Parámetros:
        -----------
        constant_value : float, default=1.0
            Valor inicial del ConstantKernel (amplitud del proceso)
        length_scale : float, default=1000.0
            Valor inicial del RBF kernel (escala de correlación espacial)
        noise_level : float, default=0.1
            Valor inicial del WhiteKernel (nivel de ruido)
        length_scale_bounds : tuple, default=(1e-5, 1e5)
            Límites para optimización del parámetro length_scale del RBF
        noise_level_bounds : tuple, default=(1e-10, 1e3)
            Límites para optimización del parámetro noise_level del WhiteKernel

        Returns:
        --------
        kernel : sklearn.gaussian_process.kernels.Kernel
            Objeto kernel listo para usar en GaussianProcessRegressor

        """

        # Kernel constante (amplitud)
        constant_kernel = ConstantKernel(constant_value, constant_value_bounds="fixed")
        # Kernel RBF (correlación espacial)
        rbf_kernel = RBF(length_scale=length_scale, length_scale_bounds=length_scale_bounds)
        # Kernel de ruido
        noise_kernel = WhiteKernel(noise_level=noise_level, noise_level_bounds=noise_level_bounds)
        # Combinar kernels: (Constante * RBF) + Ruido
        return constant_kernel * rbf_kernel + noise_kernel

    
     # Generar el modelo GaussianProcessRegressor
    def create_gpr_model(kernel: Kernel) -> GaussianProcessRegressor:
        """Instancia el GaussianProcessRegressor con el kernel dado."""
        return GaussianProcessRegressor(kernel=kernel, alpha=1e-6, n_restarts_optimizer=10)


    # -------------------------------------------------------------------------
    # 2. Fit y predicción
    # -------------------------------------------------------------------------

    def fit_gpr_model(
        gpr: GaussianProcessRegressor, 
        coords: np.ndarray, 
        values: np.ndarray
    ) -> GaussianProcessRegressor:
        """Ajusta el modelo GPR a las coordenadas y valores observados."""
        gpr.fit(coords, values)
        return gpr

    def predict_grid(
        model: GaussianProcessRegressor, 
        #grid: Tuple[np.ndarray, np.ndarray, np.ndarray]
        grid_coords: np.ndarray,          # ← recibe solo coords aplanadas, sin tupla
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predice media (z) e incertidumbre (ss) sobre una grilla de coordenadas.

        Separado de interpolate_grid para poder reutilizar
        cualquier grilla externa sin recronstruirla.
        """
        # Desempaquetar la tupla grid
        #grid_x, grid_y, _ = grid
        # Preparar puntos para predicción
        #points = np.column_stack((grid_x.ravel(), grid_y.ravel()))

        z, ss = model.predict(grid_coords, return_std=True)
        return z, ss
    




    
    
    def extract_centroids_from_gdf(gdf: gpd.GeoDataFrame, column_name: str) -> np.ndarray:
        # Extraer valores de una columna específica 
        values = gdf[column_name].values
        print(f"Rango de valores: {values.min():.2f} - {values.max():.2f}")

        return values

    def prepare_geospatial_bounds(gdf: gpd.GeoDataFrame) -> np.ndarray:

        # Obtener límites en coordenadas proyectadas
        bounds_proj = gdf.total_bounds  # [xmin, ymin, xmax, ymax]
        return bounds_proj


    # Run in main.py
    def run_kriging_pipeline(
        grid_2d_lp: np.ndarray, 
        gdf_la_plata_from_polygon: gpd.GeoDataFrame, 
        step: int = 100
    ) -> str:
        grid_lp = extract_grid_from_tuple(grid_2d_lp)
        geo_bounds_lp = prepare_geospatial_bounds(gdf_la_plata_from_polygon)
        geotiff_file = write_geotiff(
            grid_lp, 
            geo_bounds_lp, 
            'kriging_densidad_poblacional.tif', 
            32721
        )
        return geotiff_file