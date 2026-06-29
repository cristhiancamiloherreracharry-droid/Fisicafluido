import streamlit as st
from auth import iniciar_sesion, cerrar_sesion
from dashboard import mostrar_dashboard
from misiones import ejecutar_mision

# Configuración obligatoria al inicio
st.set_page_config(page_title="Misiones Física", page_icon="🌊", layout="centered", initial_sidebar_state="collapsed")

# Inyección del CSS personalizado
def cargar_css():
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Ignora si el archivo no se encuentra temporalmente

cargar_css()

# Control de estado inicial
if 'pagina' not in st.session_state: st.session_state.pagina = "dashboard"
if 'usuario' not in st.session_state: st.session_state.usuario = None

# Menú lateral colapsable (Hamburguesa en móvil)
with st.sidebar:
    st.title("Navegación 🧭")
    if st.button("🏠 Cuartel General"): st.session_state.pagina = "dashboard"
    if st.button("🚀 Inmersión (Jugar)"): st.session_state.pagina = "misiones"
    st.divider()
    if st.button("🚪 Abandonar Nave"): cerrar_sesion()

# Enrutador
if st.session_state.usuario is None:
    st.title("Misiones de Física 🤿")
    st.write("Identificación requerida para abordar.")
    email = st.text_input("Correo de Cadete")
    pwd = st.text_input("Código de Acceso", type="password")
    if st.button("Iniciar Misión"):
        iniciar_sesion(email, pwd)
else:
    pagina = st.session_state.get("pagina", "dashboard")
    if pagina == "dashboard":
        mostrar_dashboard()
    elif pagina == "misiones":
        ejecutar_mision()
