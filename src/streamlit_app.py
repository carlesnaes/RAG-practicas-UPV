# streamlit_app.py

import streamlit as st
import os
import yaml
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from indexador import construir_o_cargar_indice
from rag_chain import get_memory, recuperar_y_rerankear, generar_respuesta
from db_logger import guardar_resultado

# Cargar entorno
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    st.error("Falta la variable de entorno OPENAI_API_KEY")
    st.stop()

st.set_page_config(page_title="Asistente UPV", page_icon="🎓")
st.title("🎓 Asistente de Prácticas Externas - UPV")

# Selección de prompt desde YAML
ruta_yaml = "Prompts/prompts.yaml"
tipos_prompt = ["default", "estricto", "informal"]
prompt_seleccionado = st.selectbox("🧩 Elige tipo de prompt", tipos_prompt)

# Carga de recursos pesada: índice, memoria y cadena RAG
@st.cache_resource(show_spinner=False)
def load_resources(ruta_index, ruta_yaml, prompt_name):
    faiss_index = construir_o_cargar_indice(ruta_index)
    custom_prompt = cargar_prompt_por_nombre(ruta_yaml, prompt_name)
    return faiss_index, custom_prompt


# Función auxiliar para cargar prompt por nombre
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

# Cargar recursos solo una vez
auto_index_path = "./Code/faiss_practicas_upv"
with st.spinner("Cargando recursos..."):
    faiss_index, custom_prompt = load_resources(auto_index_path, ruta_yaml, prompt_seleccionado)


if "memory" not in st.session_state:
    st.session_state["memory"] = get_memory()

memory = st.session_state["memory"]

# Mostrar estado de memoria
if memory and memory.chat_memory.messages:
    st.write("🧠 Memoria actual:")
    for m in memory.chat_memory.messages:
        st.markdown(f"**{m.type.upper()}**: {m.content}")

# Entrada del usuario
disabled = False
query = st.text_input("Haz tu pregunta:", disabled=disabled)
enviar = st.button("Enviar")


if query and (enviar or not st.session_state.get("esperando_boton", False)):
    with st.spinner("Consultando..."):
        retriever = faiss_index.as_retriever(
            search_type="mmr", search_kwargs={"k": 15, "fetch_k": 40, "lambda_mult": 0.3}
        )
        docs_filtrados = recuperar_y_rerankear(query, retriever, usar_reranker=True)
        chat_hist = memory.chat_memory.messages
        history_formatted = [(m.type, m.content) for m in chat_hist]

        respuesta = generar_respuesta(
            llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3),
            prompt_template=custom_prompt,
            question=query,
            context_docs=docs_filtrados,
            chat_history=history_formatted
        )
        memory.chat_memory.add_user_message(query)
        memory.chat_memory.add_ai_message(respuesta)


    st.markdown("### ✅ Respuesta")
    st.write(respuesta)

    st.markdown("### 🗂️ Documentos utilizados")
    for i, doc in enumerate(docs_filtrados, start=1):
        st.markdown(f"**{i}. Fuente:** `{doc.metadata.get('source', 'desconocida')}`")
        st.write(doc.page_content)

    if st.button("💾 Guardar esta respuesta"):
        guardar_resultado(query, respuesta, docs_filtrados, history_formatted)
        st.success("Respuesta guardada correctamente.")

elif not query:
    st.session_state["esperando_boton"] = True

