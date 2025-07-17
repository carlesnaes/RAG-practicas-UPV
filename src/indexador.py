import os
import requests
from hashlib import md5
from bs4 import BeautifulSoup

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
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
    for nodo in soup.select("div.wp-block-upv-acordeon"):
        title_el = nodo.select_one("h3")
        title = title_el.get_text(strip=True) if title_el else "Sin título"
        body = nodo.find(
            "div",
            class_=lambda c: c and ("acordeon__body" in c or "closed" in c)
        )
        for a in body.find_all("a", href=True):
            link_text = a.get_text(strip=True)
            href = a['href']
            a.replace_with(f"{link_text} ({href})")
        text = body.get_text("\n", strip=True) if body else ""
        raw_docs.append(Document(
            page_content=f"## {title}\n\n{text}",
            metadata={"source": url, "role": role}
        ))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(raw_docs)


# def scrape_siepract_estudiantes(url: str, role: str):
#     """
#     Extrae contenido de la web SIE prácticas para estudiantes y devuelve chunks con metadata.
#     """
#     headers = {"User-Agent": "Mozilla/5.0"}
#     resp = requests.get(url, headers=headers, timeout=15)
#     resp.raise_for_status()
#     soup = BeautifulSoup(resp.text, "html.parser")

#     main_content = soup.find("div", class_="contenido") or soup.find("main") or soup.body
#     raw_text = main_content.get_text("\n", strip=True) if main_content else soup.get_text("\n", strip=True)

#     document = Document(
#         page_content=raw_text,
#         metadata={"source": url, "role": role}
#     )

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=250,
#         separators=["\n\n", "\n", " ", ""]
#     )
#     chunks = splitter.split_documents([document])

#     encabezado = (
#         "⚠️⚠️ Esta información aplica únicamente cuando la Universitat Politècnica de València (UPV) actúa como empresa colaboradora para las prácticas, no sirve para las empresas externas a la UPV.")
#     for chunk in chunks:
#         chunk.page_content = encabezado + chunk.page_content
#     return chunks


def scrape_creditos_horas_extra(url: str, role: str):
    """
    Extrae toda la información general (excepto la tabla) desde la web de créditos/horas.
    Ahora conserva los enlaces embebidos (Texto visible + URL).
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Encontrar el contenido general excepto la tabla
    main_content = soup.find("div", class_="contenido") or soup.find("main") or soup.body
    if main_content:
        # Eliminar tablas para no duplicar la tabla de créditos/horas
        for table in main_content.find_all("table"):
            table.decompose()

        # Procesar enlaces <a> para conservar URLs
        for a in main_content.find_all("a", href=True):
            link_text = a.get_text(strip=True)
            href = a['href']
            a.replace_with(f"{link_text} ({href})")

    raw_text = main_content.get_text("\n", strip=True) if main_content else ""

    doc = Document(
        page_content="## Información adicional sobre prácticas\n\n" + raw_text,
        metadata={"source": url, "role": role}
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=250,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents([doc])


def construir_o_cargar_indice(ruta_directorio: str = "faiss_index") -> FAISS:
    """
    Crea o actualiza incrementalmente un índice FAISS.
    Si el índice existe, añade solo los chunks nuevos (basado en checksum),
    si no, crea uno desde cero.
    """
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Carga documentos normativos, manuales y scraping
    archivos_pdf_estudiante = [
        ("./Datos/ReglamPracUPVMod2022.pdf", "normativa_estudiante.txt"),
        ("./Datos/Informacion-Practicas-Externas-ETSINF.pdf", "creditos_horas.txt")
    ]
    ruta_tabla_estudiante = "./Datos/Informacion-Practicas-Externas-ETSINF.pdf"
    archivos_pdf_empresa = [
        ("./Datos/ReglamPracUPVMod2022.pdf", "normativa_empresa.txt")
    ]
    ruta_tabla_empresa = None

    docs_est = cargar_documentos_y_tabla(
    archivos_pdf_estudiante,
    ruta_tabla_estudiante,
    role="estudiante",
    solo_tabla=True  #  solo queremos la tabla
    )
    docs_est += cargar_documentos_y_tabla([("./Datos/ReglamPracUPVMod2022.pdf", "normativa_estudiante.txt")],
    None,
    role="estudiante"
    )

    docs_est += cargar_chunks_manual(role="estudiante")
    docs_est += scrape_creditos_horas_extra(
        url="https://www.upv.es/entidades/etsinf/estudiante-2-2/",
        role="estudiante"
    )
    # docs_est += scrape_siepract_estudiantes(
    #     url="https://www.upv.es/contenidos/siepract/practicas-en-entidades-upv/",
    #     role="estudiante"
    # )

    docs_emp = cargar_documentos_y_tabla(
        archivos_pdf_empresa,
        ruta_tabla_empresa,
        role="empresa"
    )
    docs_emp += cargar_chunks_manual(role="empresa")
    docs_emp += scrape_empresa(
        url="https://www.upv.es/entidades/etsinf/empresa/",
        role="empresa"
    )

    all_docs = docs_est + docs_emp
    # Calcular checksum para cada chunk
    for doc in all_docs:
        chk = md5(doc.page_content.encode('utf-8')).hexdigest()
        doc.metadata['checksum'] = chk

    # Carga o actualización incremental del índice
    if os.path.exists(ruta_directorio):
        faiss_index = FAISS.load_local(
            ruta_directorio,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
        existing = faiss_index.docstore._dict.values()
        existing_checksums = {d.metadata.get('checksum') for d in existing}
        new_docs = [d for d in all_docs if d.metadata['checksum'] not in existing_checksums]
        if new_docs:
            faiss_index.add_documents(new_docs)
            print(f"Añadidos {len(new_docs)} chunks nuevos al índice.")
        else:
            print("No hay chunks nuevos para añadir.")
    else:
        faiss_index = FAISS.from_documents(all_docs, embeddings)
        print(f"Índice creado con {len(all_docs)} chunks.")

    faiss_index.save_local(ruta_directorio)
    return faiss_index


if __name__ == "__main__":
    construir_o_cargar_indice()
