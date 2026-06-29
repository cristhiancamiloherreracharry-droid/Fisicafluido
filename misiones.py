import streamlit as st
import requests
from streamlit_lottie import st_lottie
from motor_ia import generar_mision_completa

# Función para cargar animaciones ligeras
def cargar_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def ejecutar_mision():
    st.title("🌊 Zona de Inmersión")
    
    # URLs de animaciones vectoriales ligeras
    lottie_hunde = cargar_lottie_url("https://lottie.host/8c5b9b94-2782-4f3d-9d41-4770fc5ec07b/8D9rJ2M0Z1.json")
    lottie_flota = cargar_lottie_url("https://lottie.host/4a5b1f9b-6d38-4e89-a292-8086054be7e2/Y9mF4yA0C5.json")

    # Inicializar el estado de las fases en la sesión
    if 'fase_actual' not in st.session_state:
        st.session_state.fase_actual = 0
    if 'formula_usuario' not in st.session_state:
        st.session_state.formula_usuario = []

    tema = st.selectbox("Selecciona el simulador:", ["Densidad y Flotabilidad (El Cofre)"])
    
    if st.button("🚀 Iniciar Despliegue"):
        with st.spinner("Sincronizando coordenadas con IA..."):
            preguntas = generar_mision_completa(tema)
            if preguntas:
                st.session_state.mision_activa = preguntas[0]
                st.session_state.fase_actual = 1
                st.session_state.formula_usuario = []
                st.rerun()

    # Si hay una misión activa, ejecutamos la máquina de estados
    if 'mision_activa' in st.session_state and st.session_state.fase_actual > 0:
        mision = st.session_state.mision_activa
        
        st.divider()
        st.info(f"**Misión:** {mision['enunciado']}")
        
        # ---------------------------------------------------------
        # FASE 1: EXTRACCIÓN DE DATOS
        # ---------------------------------------------------------
        st.write("### Fase 1: Escaneo de Variables")
        col1, col2 = st.columns(2)
        masa_input = col1.number_input("Masa (kg)", min_value=0.0, step=1.0)
        vol_input = col2.number_input("Volumen (m3)", min_value=0.0, step=0.1)
        
        if st.session_state.fase_actual == 1:
            if st.button("Validar Extracción"):
                if masa_input == mision['masa'] and vol_input == mision['volumen']:
                    st.success("¡Datos extraídos correctamente! Se habilita la computadora de a bordo.")
                    st.session_state.fase_actual = 2
                    st.rerun()
                else:
                    st.error("Error en el radar. Revisa los números del enunciado.")

        # ---------------------------------------------------------
        # FASE 2: PLANTEAMIENTO DE LA FÓRMULA
        # ---------------------------------------------------------
        if st.session_state.fase_actual >= 2:
            st.divider()
            st.write("### Fase 2: Computadora de Navegación")
            st.write("Arma la fórmula de la Densidad tocando los botones:")
            
            # Botones táctiles para armar la ecuación
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("Masa"): st.session_state.formula_usuario.append("Masa")
            if c2.button("Volumen"): st.session_state.formula_usuario.append("Volumen")
            if c3.button(" ➕ "): st.session_state.formula_usuario.append("+")
            if c4.button(" ➗ "): st.session_state.formula_usuario.append("/")
            
            # Mostrar lo que el cadete va armando
            st.info(f"Tu fórmula: **{' '.join(st.session_state.formula_usuario)}**")
            
            if st.button("Limpiar Fórmula"):
                st.session_state.formula_usuario = []
                st.rerun()

            if st.session_state.fase_actual == 2:
                if st.button("Validar Fórmula"):
                    if st.session_state.formula_usuario == ["Masa", "/", "Volumen"]:
                        st.success("¡Enrutamiento lógico perfecto! Motor de cálculo desbloqueado.")
                        st.session_state.fase_actual = 3
                        st.rerun()
                    else:
                        st.error("Esa no es la fórmula de la densidad. Piensa en la relación entre masa y espacio.")

        # ---------------------------------------------------------
        # FASE 3: EJECUCIÓN Y CONSECUENCIA VISUAL
        # ---------------------------------------------------------
        if st.session_state.fase_actual == 3:
            st.divider()
            st.write("### Fase 3: Ejecución")
            st.write("Usa tu calculadora física y digita el resultado final:")
            
            resultado_final = st.number_input("Densidad del objeto (kg/m3)", min_value=0.0, step=1.0)
            
            if st.button("Confirmar Acción"):
                if resultado_final == mision['respuesta_correcta']:
                    estado = mision['estado_final']
                    if estado == "se hunde":
                        st.success(f"¡Cálculo exacto ({resultado_final})! El objeto supera la densidad del mar.")
                        if lottie_hunde:
                            st_lottie(lottie_hunde, height=200, key="hunde")
                    else:
                        st.warning(f"¡Cálculo exacto ({resultado_final})! El objeto es más ligero que el mar.")
                        if lottie_flota:
                            st_lottie(lottie_flota, height=200, key="flota")
                    
                    st.balloons() # Recompensa visual nativa de Streamlit
                else:
                    st.error("El cálculo numérico tiene una desviación. Vuelve a hacer la división.")
