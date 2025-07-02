# streamlit_app.py (versión rediseñada estilo chat moderno)

import streamlit as st
import os
import yaml
from dotenv import load_dotenv
from datetime import datetime as dt
from langchain.prompts import PromptTemplate

from indexador import construir_o_cargar_indice
from rag_chain import get_memory, crear_rag_chain



# Configuración general
st.set_page_config(page_title="Asistente UPV", page_icon="🎓", layout="centered")

# Inicializar flags de sesión antes de todo
if "pending_answer" not in st.session_state:
    st.session_state.pending_answer = False

if "memory" not in st.session_state:
    st.session_state.memory = get_memory()

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "message": "Hola 👋 Soy el asistente de prácticas externas de la ETSINF-UPV. ¿En qué puedo ayudarte?",
        "timestamp": dt.now().strftime("%H:%M:%S")
    }]



st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    .stButton > button {
        background-color: #6A1B9A;
        color: white;
        border-radius: 10px;
        padding: 0.4em 1.2em;
    }
    </style>
""", unsafe_allow_html=True)

#  Cargar entorno y API key
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    st.error("Falta la variable de entorno OPENAI_API_KEY")
    st.stop()

# 🔧 Cargar índice y prompt
@st.cache_resource(show_spinner=False)
def load_resources(ruta_index, ruta_yaml, prompt_name):
    faiss_index = construir_o_cargar_indice(ruta_index)
    custom_prompt = cargar_prompt_por_nombre(ruta_yaml, prompt_name)
    return faiss_index, custom_prompt

@st.cache_resource(show_spinner=False)
def cargar_prompt_por_nombre(ruta_yaml, nombre):
    with open(ruta_yaml, "r", encoding="utf-8") as f:
        prompts = yaml.safe_load(f).get("prompts", [])
    for p in prompts:
        if p.get("name") == nombre:
            return PromptTemplate(
                input_variables=["context", "question", "chat_history"],
                template=p.get("template", "")
            )
    raise ValueError(f"No se encontró el prompt con nombre: {nombre}")

# Cargar recursos una vez
auto_index_path = "./Code/faiss_practicas_upv"
ruta_yaml = "Prompts/prompts.yaml"
prompt_seleccionado = "estricto"
with st.spinner("Cargando recursos..."):
    faiss_index, custom_prompt = load_resources(auto_index_path, ruta_yaml, prompt_seleccionado)

if "memory" not in st.session_state:
    st.session_state.memory = get_memory()

rag_chain = crear_rag_chain(faiss_index, st.session_state.memory, custom_prompt)

#  Inicializar historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "message": "Hola 👋 Soy el asistente de prácticas externas de la ETSINF-UPV. ¿En qué puedo ayudarte?",
        "timestamp": dt.now().strftime("%H:%M:%S")
    }]

#  Botón para limpiar conversación
col1, col2 = st.columns([5, 1])
with col1:
    st.subheader("🎓 Asistente de Prácticas Externas - UPV", divider="gray")
with col2:
    if st.button("🧹 Limpiar chat"):
        st.session_state.messages = []
        st.session_state.memory = get_memory()
        st.rerun()

# Mostrar conversación
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["message"])

# Entrada del usuario (input chat)
if user_input := st.chat_input("Escribe tu pregunta..."):
    timestamp = dt.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "user",
        "message": user_input,
        "timestamp": timestamp
    })
    st.session_state.pending_answer = True  # Marcar que hay respuesta pendiente
    st.rerun()

# Procesar respuesta del asistente solo si está pendiente
if st.session_state.pending_answer:
    ultima_pregunta = st.session_state.messages[-1]["message"]
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                result = rag_chain.invoke({"question": ultima_pregunta})
                respuesta = result["answer"]
                documentos = result["source_documents"]
            except Exception as e:
                respuesta = f"⚠️ Error generando respuesta: {e}"
                documentos = []

        st.write(respuesta)

        if documentos:
            with st.expander("📂 Ver documentos utilizados"):
                for i, doc in enumerate(documentos):
                    st.markdown(f"**{i+1}. Fuente:** `{doc.metadata.get('source', 'desconocida')}`")
                    st.write(doc.page_content)

    # Guardar y marcar como respondido
    st.session_state.messages.append({
        "role": "assistant",
        "message": respuesta,
        "timestamp": dt.now().strftime("%H:%M:%S")
    })

    chat_hist = st.session_state.memory.chat_memory.messages
    formatted_hist = [(m.type, m.content) for m in chat_hist]
    
    st.session_state.pending_answer = False
