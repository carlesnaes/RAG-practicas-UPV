import sqlite3
import numpy as np



def serializar_chat(chat_history):
    return "\n".join(f"{role.upper()}: {msg}" for role, msg in chat_history)

def guardar_resultado(pregunta, respuesta, contexto_docs, chat_history):
    contexto_completo = "\n---\n".join(doc.page_content for doc in contexto_docs)
    chat_serializado = serializar_chat(chat_history)

    conn = sqlite3.connect("./Code/rag_respuestas.db")  
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO rag_logs (pregunta, respuesta, contexto, chat_history)
        VALUES (?, ?, ?, ?)
    """, (pregunta, respuesta, contexto_completo, chat_serializado))

    conn.commit()
    conn.close()  


def cosine_similarity(vec1, vec2):
    """
    Calcula la similitud coseno entre dos vectores.
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def buscar_en_base_datos(pregunta, db_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar coincidencia exacta en logs (última respuesta registrada)
    cursor.execute("""
        SELECT respuesta FROM rag_logs 
        WHERE pregunta = ? 
        ORDER BY id DESC LIMIT 1
    """, (pregunta,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        print("✅ Coincidencia encontrada en rag_logs")
        return row[0]
    else:
        print("❌ No encontrada en rag_logs")
        return None

