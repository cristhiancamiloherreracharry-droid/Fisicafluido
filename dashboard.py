import streamlit as st

def mostrar_dashboard():
    st.title("Cuartel General 🏠")
    
    # Simulación de datos (En el futuro, esto consultará a Supabase)
    misiones_completadas = 2
    total_misiones = 5
    
    # Barra de progreso circular o lineal elegante
    progreso = misiones_completadas / total_misiones
    st.write("### Tu avance global")
    st.progress(progreso)
    st.write(f"Has completado {misiones_completadas} de {total_misiones} misiones de entrenamiento.")
    
    # Sección de "Insignias" con columnas
    st.write("### Tus Logros")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nivel", "1")
    col2.metric("Racha", "3 días")
    col3.metric("Puntos", "150")
