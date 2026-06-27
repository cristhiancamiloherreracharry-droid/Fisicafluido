import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def obtener_cliente_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def iniciar_sesion(email, password):
    supabase = obtener_cliente_supabase()
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user_id = response.user.id
        
        perfil = supabase.table("perfiles").select("rol, nombre").eq("id", user_id).execute()
        
        if perfil.data:
            st.session_state.usuario = perfil.data[0]['nombre']
            st.session_state.rol = perfil.data[0]['rol']
            st.session_state.user_id = user_id
            st.rerun() 
    except Exception as e:
        # Aquí pusimos el error detallado para saber qué falla en la conexión
        st.error(f"Error detallado: {e}")

def cerrar_sesion():
    supabase = obtener_cliente_supabase()
    supabase.auth.sign_out()
    st.session_state.usuario = None
    st.session_state.rol = None
    st.session_state.user_id = None
    st.rerun()
