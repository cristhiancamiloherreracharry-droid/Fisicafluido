import streamlit as st
from auth import iniciar_sesion, cerrar_sesion
from motor_ia import generar_mision_gemini

# Configuración de página
st.set_page_config(page_title="Misiones de Física", page_icon="🚀", layout="centered")

# Inicialización de estado de sesión
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
    st.session_state.rol = None
    st.session_state.user_id = None

def vista_login():
    st.title("Bienvenido a Misiones de Física 🤿🚢")
    st.write("Ingresa tus credenciales para comenzar.")
    
    with st.form("login_form"):
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar Misión")
        
        if submit:
            iniciar_sesion(email, password)

def vista_estudiante():
    st.success(f"¡Hola, {st.session_state.usuario}! Misión lista para comenzar.")
    
    # Menú desplegable para que el estudiante elija (o podemos hacerlo aleatorio luego)
    tema = st.selectbox("Selecciona tu misión de hoy:", [
        "Presión Hidrostática", 
        "Principio de Arquímedes", 
        "Presión Básica de Fluidos",
        "Densidad y Flotabilidad"
    ])
    
    # Botón para detonar el motor de IA
    if st.button("Solicitar Misión a la IA"):
        with st.spinner("Conectando con el comando central y calculando variables..."):
            preguntas = generar_mision_gemini(tema)
            if preguntas:
                st.write("### Datos recibidos de Gemini:")
                st.json(preguntas) # Renderiza el JSON crudo temporalmente para validar que la estructura es perfecta
    
    st.divider()
    if st.button("Cerrar Sesión"):
        cerrar_sesion()

def vista_admin():
    st.info(f"Panel de Control - Administrador ({st.session_state.usuario})")
    st.write("Métricas de rendimiento de estudiantes en construcción.")
    
    st.divider()
    if st.button("Cerrar Sesión"):
        cerrar_sesion()

# Enrutador principal
if st.session_state.usuario is None:
    vista_login()
else:
    if st.session_state.rol == 'admin':
        vista_admin()
    elif st.session_state.rol == 'estudiante':
        vista_estudiante()
