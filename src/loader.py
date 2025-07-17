import pdfplumber
from langchain.document_loaders import TextLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import fitz  # PyMuPDF
import os


def extraer_texto_pdf(ruta_pdf):
    print('La ruta actual es:', os.getcwd())
    doc = fitz.open(ruta_pdf)
    texto = ""

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        span_text = span["text"]
                        # Verificar si el texto tiene un enlace asociado
                        link_found = False
                        for link in page.get_links():
                            bbox = link["from"]  # Bounding box del enlace
                            if fitz.Rect(span["bbox"]).intersects(fitz.Rect(bbox)):
                                href = link.get("uri", "")
                                if href:
                                    # Añadir la URL en formato " (url: ...)"
                                    span_text += f" (url: {href})"
                                    link_found = True
                        texto += span_text
                    texto += "\n"
        texto += "\n"
    return texto


def cargar_documentos_y_tabla(archivos_pdf, ruta_tabla_pdf, role, solo_tabla=False):
    docs = []

    if not solo_tabla:
        # Procesar archivos PDF genéricos (extraer texto completo y dividir en chunks)
        for ruta_pdf, nombre_txt in archivos_pdf:
            texto = extraer_texto_pdf(ruta_pdf)
            with open(f"./Datos/{nombre_txt}", "w", encoding="utf-8") as f:
                f.write(texto)

            loader = TextLoader(f"./Datos/{nombre_txt}", encoding="utf-8")
            loaded = loader.load()
            for doc in loaded:
                doc.metadata["source"] = nombre_txt
                doc.metadata["role"] = role
            docs.extend(loaded)

        # Dividir en chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        text_chunks = splitter.split_documents(docs)
    else:
        # Si solo_tabla=True, no añadir texto ni generar chunks
        text_chunks = []

    # Procesar tabla de créditos-horas si existe
    tabla_docs = []
    if ruta_tabla_pdf:
        filas = []
        with pdfplumber.open(ruta_tabla_pdf) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables():
                    for row in table:
                        filas.append(row)

        for fila in filas[1:]:
            if len(fila) >= 3:
                titulacion = fila[0].replace("\n", " ").strip()
                curriculares = fila[1].strip()
                extracurriculares = fila[2].strip()
                contenido = (
                    f"Información oficial sobre el número de horas de prácticas permitidas en la titulación de {titulacion}, según la normativa de la Universitat Politècnica de València (UPV). "
                    f"Los estudiantes matriculados en este grado o máster pueden realizar prácticas externas en "
                    f"{'modalidad prácticas extracurriculares' if 'doble grado' in titulacion.lower() else 'dos modalidades: prácticas curriculares y extracurriculares'}. "
                    f"{'' if 'doble grado' in titulacion.lower() else f'Las prácticas curriculares están limitadas a {curriculares}, y forman parte del plan de estudios oficial, computando créditos ECTS. '} "
                    f"Las extracurriculares, que {'son voluntarias' if 'doble grado' in titulacion.lower() else 'son voluntarias y no curriculares'}, tienen un máximo de {extracurriculares}. "
                    f"Esta información está basada en la tabla oficial de equivalencia de créditos y horas por titulación, y es válida para la planificación de las prácticas en empresa."
                )

                doc = Document(
                    page_content=contenido,
                    metadata={
                        "source": "tabla créditos-horas",
                        "role": role
                    }
                )
                tabla_docs.append(doc)

    return text_chunks + tabla_docs


    return text_chunks + tabla_docs
