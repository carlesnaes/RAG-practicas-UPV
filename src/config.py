# config.py

# Lista de archivos a procesar
archivos_pdf = [
    ("../Datos/ReglamPracUPVMod2022.pdf", "normativa.txt"),
    ("../Datos/Informacion-Practicas-Externas-ETSINF.pdf", "creditos_horas.txt")
]

# Ruta a un PDF específico
ruta_tabla_pdf = "../Datos/Informacion-Practicas-Externas-ETSINF.pdf"

# Solo el nombre del modelo, esto es configuración pura.
embedding_model_name = "sentence-transformers/all-mpnet-base-v2"