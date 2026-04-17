
class KrigingModel:
    def __init__(self):
        pass

     # Función para crear un kernel de Kriging
    def create_kriging_kernel(constant_value=1.0, length_scale=1000.0, noise_level=0.1,
                             length_scale_bounds=(1e-5, 1e5), noise_level_bounds=(1e-10, 1e3)):
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
        kernel = constant_kernel * rbf_kernel + noise_kernel

        return kernel