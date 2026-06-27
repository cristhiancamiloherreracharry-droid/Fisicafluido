import google.generativeai as genai
import json
import streamlit as st

# Configuración inicial de Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generar_mision_gemini(tema_elegido):
    """
    Genera 5 preguntas de física estructuradas en JSON usando Gemini 1.5 Flash.
    """
    model = genai.GenerativeModel(
        'gemini-1.5-flash', 
        generation_config={"response_mime_type": "application/json"}
    )
    
    prompt = f"""
    Actúa como un profesor de física experto en gamificación para un estudiante de octavo grado (13 años).
    Genera 5 preguntas interactivas sobre el tema: {tema_elegido}.
    
    Reglas físicas a aplicar según el tema:
    1. Presión Hidrostática (Buzos y Submarinos): P = d * g * h. (Usa g=9.8. Respuesta en Pascales).
    2. Principio de Arquímedes (Barcos y Empuje): E = d * V * g. (Agua dulce d=1000, salada d=1025).
    3. Presión Básica de Fluidos (Tuberías y Presas): P = F / A.
    4. Densidad y Flotabilidad (Misterio del Cofre): d = m / V. (Regla: si d < 1000 flota, si > 1000 se hunde).
    
    Devuelve estrictamente un arreglo JSON con esta estructura exacta para cada pregunta:
    [
      {{
        "enunciado": "Texto gamificado (ej. Eres el capitán de un submarino y desciendes a 50 metros...)",
        "variables": {{"profundidad": 50, "densidad": 1025, "gravedad": 9.8}},
        "respuesta_correcta": 502250, 
        "tipo_resultado": "numero", 
        "explicacion": "Explicación breve de cómo aplicar la fórmula para llegar al resultado."
      }}
    ]
    """
    
    try:
        respuesta = model.generate_content(prompt)
        preguntas = json.loads(respuesta.text)
        return preguntas
    except Exception as e:
        st.error(f"Error en la capa de inferencia (IA): {e}")
        return []
