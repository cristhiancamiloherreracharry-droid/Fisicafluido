import streamlit as st
from supabase import create_client, Client

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Misiones de Física", page_icon="🚀", layout="centered")

# --- CONEXIÓN A SUPABASE ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase: Client = init_connection()

# --- INICIALIZACIÓN DE SESIÓN ---
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'rol' not in st.session_state:
    st.session_state.rol = None

# --- FUNCIONES DE AUTENTICACIÓN ---
def iniciar_sesion(email, password):
    try:
        # Autenticar con Supabase
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user_id = response.user.id
        
        # Consultar el rol en la tabla perfiles
        perfil = supabase.table("perfiles").select("rol, nombre").eq("id", user_id).execute()
        
        if perfil.data:
            st.session_state.usuario = perfil.data[0]['nombre']
            st.session_state.rol = perfil.data[0]['rol']
            st.rerun() # Recarga la app con la nueva sesión
    except Exception as e:
        st.error("Credenciales incorrectas o error de conexión.")

def cerrar_sesion():
    supabase.auth.sign_out()
    st.session_state.usuario = None
    st.session_state.rol = None
    st.rerun()

# --- VISTAS (RUTAS) ---
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
    # Aquí irá la lógica de las 5 preguntas y Gemini
    st.write("Generando entorno de simulación...")
    if st.button("Cerrar Sesión"):
        cerrar_sesion()

def vista_admin():
    st.info(f"Panel de Control - Administrador ({st.session_state.usuario})")
    # Aquí irá el dashboard de analíticas
    st.write("Métricas de rendimiento de estudiantes.")
    if st.button("Cerrar Sesión"):
        cerrar_sesion()

# --- ENRUTADOR PRINCIPAL ---
if st.session_state.usuario is None:
    vista_login()
else:
    if st.session_state.rol == 'admin':
        vista_admin()
    elif st.session_state.rol == 'estudiante':
        vista_estudiante()
