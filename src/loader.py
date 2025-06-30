# loader.py

import pdfplumber
from langchain.document_loaders import TextLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF
import os


def extraer_texto_pdf(ruta_pdf):
    print('La ruta actual es:',os.getcwd())
    doc = fitz.open(ruta_pdf)
    texto = ""
    for page in doc:
        texto += page.get_text()
    return texto

def cargar_documentos_y_tabla(archivos_pdf, ruta_tabla_pdf):
    docs = []
    for ruta_pdf, nombre_txt in archivos_pdf:
        texto = extraer_texto_pdf(ruta_pdf)
        with open(f"./Datos/{nombre_txt}", "w", encoding="utf-8") as f:
            f.write(texto)

        loader = TextLoader(f"./Datos/{nombre_txt}", encoding="utf-8")
        loaded = loader.load()
        for doc in loaded:
            doc.metadata["source"] = nombre_txt
        docs.extend(loaded)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    text_chunks = splitter.split_documents(docs)

    # Cargar tabla del PDF
    filas = []
    with pdfplumber.open(ruta_tabla_pdf) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    filas.append(row)

    tabla_docs = []
    for fila in filas[1:]:
        if len(fila) >= 3:
            titulacion = fila[0].replace("\n", " ").strip()
            curriculares = fila[1].strip()
            extracurriculares = fila[2].strip()
            contenido = (
                f"Información oficial sobre el número de horas de prácticas permitidas en la titulación de {titulacion}, según la normativa de la Universitat Politècnica de València (UPV). "
                f"Los estudiantes matriculados en este grado o máster pueden realizar prácticas externas en dos modalidades: prácticas curriculares y prácticas extracurriculares. "
                f"Las prácticas curriculares están limitadas a {curriculares}, y forman parte del plan de estudios oficial, computando créditos ECTS. "
                f"En cambio, las prácticas extracurriculares, que son voluntarias y no curriculares, tienen un máximo de {extracurriculares}. "
                f"Estas cifras representan el tope de horas que un estudiante puede realizar en cada tipo de práctica. "
                f"Esta información está basada en la tabla oficial de equivalencia de créditos y horas por titulación, y es válida para la planificación de las prácticas en empresa."
            )
            doc = Document(page_content=contenido, metadata={"source": "tabla créditos-horas"})
            tabla_docs.append(doc)

    return text_chunks + tabla_docs