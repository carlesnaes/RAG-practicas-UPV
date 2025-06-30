import sqlite3




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
