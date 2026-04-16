import streamlit as st

from fastapi import FastAPI
from flood_density.pipeline import run_flood_pipeline
from flood_density.plots import plot_kriging_results_with_basemap

# Initialize FastAPI app
app = FastAPI()

# Streamlit UI
grad = """
<style>
.gradient-text {
  font-size: 48px;
  font-weight: 800;
  background: linear-gradient(90deg, #f403d1, #04c2c9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
"""

st.markdown(grad, unsafe_allow_html=True)
st.markdown('<div class="gradient-text">¡Hola!</div>', unsafe_allow_html=True)

st.write("Le damos la bienvenida a la Aplicación de Detección de Inundaciones en la Ciudad de La Plata!")


# --------- Pipeline --------------------------
flood_data = run_flood_pipeline(
    gdf_coordinates=gdf_lp_coordinates,
    gdf_peligrosidad=gdf_peligrosidad,
    casco_urbano_utm=casco_urbano_utm,
    gdf_polygon=gdf_la_plata_from_polygon,
    gpr_model=gpr_model_kriging,
    predict_grid=predict_grid_lp,
    grid_step=100,
)


#plot_kriging_results_with_basemap(casco_urbano_utm, coordinates_lp, centroids_lp, bounds_lp, grid_x, grid_y, gpr_kriging_fit, grid_2d_lp)