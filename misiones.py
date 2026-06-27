Python
import streamlit as st
from motor_ia import generar_mision

def ejecutar_mision():
    st.title("Área de Entrenamiento 🚀")
    tema = st.selectbox("Elige tema:", ["Densidad", "Arquímedes", "Presión"])
    if st.button("Generar Desafío"):
        st.session_state.mision = generar_mision(tema)
        
    if 'mision' in st.session_state:
        # Aquí crearíamos los botones táctiles en la siguiente iteración
        st.write("¡Misión cargada! (Implementaremos la calculadora aquí)")
