import os
import requests
from bs4 import BeautifulSoup

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from man_chunks import cargar_chunks_manual
from loader import cargar_documentos_y_tabla


def scrape_empresa(url: str, role: str):
    """
    Extrae secciones de la página de la ETSINF para empresas y devuelve chunks con metadata de rol.
    Conserva los enlaces embebidos (Texto visible + URL).
    """
    headers = {"User-Agent": "Mozilla/5.0 (Jupyter; Python)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    raw_docs = []
    # Selecciona cada acordeón de la web
    for nodo in soup.select("div.wp-block-upv-acordeon"):
        title_el = nodo.select_one("h3")
        title = title_el.get_text(strip=True) if title_el else "Sin título"
        body = nodo.find(
            "div",
            class_=lambda c: c and ("acordeon__body" in c or "closed" in c)
        )

        # 🔥 Sustituye cada enlace embebido <a> por: Texto visible (URL)
        for a in body.find_all("a", href=True):
            link_text = a.get_text(strip=True)
            href = a['href']
            a.replace_with(f"{link_text} ({href})")

        # Extraer texto con los enlaces embebidos modificados
        text = body.get_text("\n", strip=True) if body else ""

        raw_docs.append(Document(
            page_content=f"## {title}\n\n{text}",
            metadata={"source": url, "role": role}
        ))

    # Dividir en chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(raw_docs)


def construir_o_cargar_indice(ruta_directorio: str = "faiss_index") -> FAISS:
    # Configurar embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cpu"}
    )

    # Si ya existe el índice, cargarlo
    if os.path.exists(ruta_directorio):
        return FAISS.load_local(
            ruta_directorio,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )

    # Definición de fuentes de documentos por rol
    archivos_pdf_estudiante = [
        ("./Datos/ReglamPracUPVMod2022.pdf", "normativa_estudiante.txt"),
        ("./Datos/Informacion-Practicas-Externas-ETSINF.pdf", "creditos_horas.txt")
    ]
    ruta_tabla_estudiante = "./Datos/Informacion-Practicas-Externas-ETSINF.pdf"

    archivos_pdf_empresa = [
        ("./Datos/ReglamPracUPVMod2022.pdf", "normativa_empresa.txt")
    ]
    ruta_tabla_empresa = None

    # Carga y chunkeo para estudiante
    docs_est = cargar_documentos_y_tabla(
        archivos_pdf_estudiante,
        ruta_tabla_estudiante,
        role="estudiante"
    )
    docs_est += cargar_chunks_manual(role="estudiante")

    # Carga y chunkeo para empresa
    docs_emp = cargar_documentos_y_tabla(
        archivos_pdf_empresa,
        ruta_tabla_empresa,
        role="empresa"
    )
    docs_emp += cargar_chunks_manual(role="empresa")
    # Añadir chunks obtenidos por web scraping
    docs_emp += scrape_empresa(
        url="https://www.upv.es/entidades/etsinf/empresa/",
        role="empresa"
    )

    # Unión final e indexación
    all_docs = docs_est + docs_emp
    faiss_index = FAISS.from_documents(
        all_docs,
        embeddings
    )
    faiss_index.save_local(ruta_directorio)
    return faiss_index
