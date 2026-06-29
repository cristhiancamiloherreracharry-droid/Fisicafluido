import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def iniciar_sesion(email, password):
    try:
        supabase = get_supabase()
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        perfil = supabase.table("perfiles").select("rol, nombre").eq("id", response.user.id).execute()
        
        if perfil.data:
            st.session_state.usuario = perfil.data[0]['nombre']
            st.session_state.rol = perfil.data[0]['rol']
            st.session_state.user_id = response.user.id
            st.rerun()
        else:
            st.warning("Usuario autenticado, pero sin registro en tabla 'perfiles'.")
    except Exception as e:
        st.error(f"Credenciales incorrectas. (Error interno: {e})")

def cerrar_sesion():
    st.session_state.clear()
    st.rerun()
