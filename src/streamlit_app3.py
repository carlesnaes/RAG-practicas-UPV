import streamlit as st
import os
import yaml
from dotenv import load_dotenv
from datetime import datetime as dt
from langchain.prompts import PromptTemplate
import openai

from indexador import construir_o_cargar_indice
from rag_chain import get_memory, crear_rag_chain


st.set_page_config(page_title="Asistente UPV", page_icon="🎓", layout="centered")
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("Falta la variable OPENAI_API_KEY en .env")
    st.stop()

if "memory" not in st.session_state:
    st.session_state.memory = get_memory()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "message": "Hola 👋 Soy el asistente de prácticas externas de la ETSINF-UPV. ¿En qué puedo ayudarte?",
            "timestamp": dt.now().strftime("%H:%M:%S"),
        }
    ]
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

# Selección de rol (Estudiante / Empresa)
role = st.sidebar.selectbox("Selecciona el perfil:", ["estudiante", "empresa"])

# Mostrar información contextual según el rol
if role == "estudiante":
    st.sidebar.info(
        "ℹ️ Para más información sobre normativa y requisitos de prácticas de estudiantes, visita "
        "[Página Estudiantes ETSINF-UPV](https://www.upv.es/entidades/etsinf/estudiante-2-2/)\n"
        "Asegúrate de revisar los **requisitos** y **procedimientos**."
    )
else:
    st.sidebar.info(
        "ℹ️ Para más información dirigida a empresas, visita "
        "[Página Empresas ETSINF-UPV](https://www.upv.es/entidades/etsinf/empresa/)\n"
    )


@st.cache_resource(show_spinner=False)
def init_chain(role):
    faiss_index = construir_o_cargar_indice("./Code/faiss_practicas_upv")
    with open("Prompts/prompts.yaml", "r", encoding="utf-8") as f:
        prompts = yaml.safe_load(f).get("prompts", [])
    # Elige el nombre de prompt según el rol
    prompt_name = f"estricto_{role}"
    template = next((p["template"] for p in prompts if p.get("name") == prompt_name), None)
    if template is None:
        raise ValueError(f"No se encontró el prompt '{prompt_name}'.")
    prompt = PromptTemplate(
        input_variables=["context", "question", "chat_history"],
        template=template,
    )
    
    return crear_rag_chain(faiss_index, st.session_state.memory, prompt, role)

rag_chain = init_chain(role)


st.title("🎓 Asistente de Prácticas Externas - UPV")

def clear_chat():
    st.session_state.memory = get_memory()
    st.session_state.messages = []
    st.session_state.last_audio = None
st.button("🧹 Limpiar chat", on_click=clear_chat)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["message"])

tab_text, tab_voice = st.tabs(["✏️ Texto", "🎤 Voz"])

with tab_text:
    if user_text := st.chat_input("Escribe tu pregunta..."):
        st.session_state.messages.append({
            "role": "user",
            "message": user_text,
            "timestamp": dt.now().strftime("%H:%M:%S"),
        })
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    out = rag_chain.invoke({"question": user_text})
                    answer = out.get("answer", "⚠️ Sin respuesta.")
                    docs = out.get("source_documents", [])
                except Exception as e:
                    answer = f"⚠️ Error: {e}"
                    docs = []
                st.write(answer)
                if docs:
                    with st.expander("📂 Documentos utilizados"):
                        for i, d in enumerate(docs, 1):
                            st.markdown(f"**{i}. Fuente:** `{d.metadata.get('source','desconocida')}`")
                            st.write(d.page_content)
        st.session_state.messages.append({
            "role": "assistant",
            "message": answer,
            "timestamp": dt.now().strftime("%H:%M:%S"),
        })

with tab_voice:
    st.info("Pulsa **Grabar** y di tu pregunta (máximo ~30s)")
    audio_data = st.audio_input(label="Grabar pregunta")
    if audio_data is not None and audio_data != st.session_state.last_audio:
        st.session_state.last_audio = audio_data
        with st.spinner("Transcribiendo…"):
            audio_result = openai.audio.transcriptions.create(
                file=audio_data,
                model="whisper-1"
            )
            transcript = audio_result.text.strip()
        st.write("🗣️", transcript)
        st.session_state.messages.append({
            "role": "user",
            "message": transcript,
            "timestamp": dt.now().strftime("%H:%M:%S"),
        })
        with st.chat_message("assistant"):
            with st.spinner("Pensando…"):
                try:
                    out = rag_chain.invoke({"question": transcript})
                    answer = out.get("answer", "⚠️ Sin respuesta.")
                    docs = out.get("source_documents", [])
                except Exception as e:
                    answer = f"⚠️ Error: {e}"
                    docs = []
                st.write(answer)
                if docs:
                    with st.expander("📂 Documentos utilizados"):
                        for i, d in enumerate(docs, 1):
                            st.markdown(f"**{i}. Fuente:** `{d.metadata.get('source','desconocida')}`")
                            st.write(d.page_content)
        st.session_state.messages.append({
            "role": "assistant",
            "message": answer,
            "timestamp": dt.now().strftime("%H:%M:%S"),
        })
