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
flood_data = run_flood_pipeline
casco_urbano = clip_density_to_urban_area(gdf_lp_coordinates,gdf_peligrosidad)
coordinates_lp = extract_coords_from_geometry(casco_urbano_utm)
centroids_lp = extract_centroids_from_gdf(casco_urbano_utm, 'Z')
bounds_lp = gdf_la_plata_from_polygon.total_bounds 
grid_x, grid_y, grid_coords = interpolate_grid(bounds_lp, step=100)
gpr_kriging_fit = fit_gpr_model(gpr_model_kriging, coordinates_lp, centroids_lp)
grid_2d_lp = convert_to_2d_grid(predict_grid_lp, grid_x.shape)

#plot_kriging_results_with_basemap(casco_urbano_utm, coordinates_lp, centroids_lp, bounds_lp, grid_x, grid_y, gpr_kriging_fit, grid_2d_lp)