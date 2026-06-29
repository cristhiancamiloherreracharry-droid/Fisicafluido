import google.generativeai as genai
import json
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generar_mision_completa(tema):
    model = genai.GenerativeModel(
        'gemini-1.5-flash', 
        generation_config={"response_mime_type": "application/json"}
    )
    
    prompt = f"""
    Eres el Comandante de una misión científica. Diseña 1 desafío sobre: {tema} para un cadete de 13 años.
    Usa mecánicas gamificadas. El tema es estrictamente "Densidad y Flotabilidad (El Cofre)".
    
    Devuelve estrictamente un arreglo JSON con 1 objeto con esta estructura exacta:
    [
      {{
        "enunciado": "Eres un buzo buscando un tesoro. Encuentras un cofre de oro con una masa de X kg y un volumen de Y m3. ¿Cuál es su densidad y qué pasará si lo sueltas en el mar?",
        "masa": X,
        "volumen": Y,
        "respuesta_correcta": Z, 
        "estado_final": "se hunde" // o "flota", dependiendo de si Z es mayor o menor a 1025 (densidad del mar).
      }}
    ]
    """
    
    try:
        respuesta = model.generate_content(prompt)
        return json.loads(respuesta.text)
    except Exception as e:
        st.error(f"Interferencia en la comunicación con el Comando Central: {e}")
        return None
