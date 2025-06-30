import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from man_chunks import cargar_chunks_manual
from loader import cargar_documentos_y_tabla


def construir_o_cargar_indice(ruta_directorio="faiss_index"):
    # Configurar embeddings para usar low_cpu_mem_usage y device_map
        # Ojo: SentenceTransformer sólo acepta 'device', no device_map/low_cpu_mem_usage
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cpu"}  # o "cuda" si tienes GPU disponible
    )

    

    if os.path.exists(ruta_directorio):
        # Carga el índice ya existente sin volver a mover tensores meta
        return FAISS.load_local(
            ruta_directorio,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )

    # Si no existe, construye nuevo índice
    archivos_pdf = [
        ("./Datos/ReglamPracUPVMod2022.pdf", "normativa.txt"),
        ("./Datos/Informacion-Practicas-Externas-ETSINF.pdf", "creditos_horas.txt")
    ]
    ruta_tabla_pdf = "./Datos/Informacion-Practicas-Externas-ETSINF.pdf"

    # Cargar y dividir documentos
    docs = cargar_documentos_y_tabla(archivos_pdf, ruta_tabla_pdf)
    docs += cargar_chunks_manual()

    # Construir índice con las mismas opciones de embeddings
    faiss_index = FAISS.from_documents(
        docs,
        embeddings
    )
    faiss_index.save_local(ruta_directorio)
    return faiss_index