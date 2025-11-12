import streamlit as st

from fastapi import FastAPI


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
st.markdown('<div class="gradient-text">Hola, personita curiosa!</div>', unsafe_allow_html=True)

st.write("Le damos la bienvenida a la Aplicación de Detección de Inundaciones!")
