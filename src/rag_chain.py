from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from reranker import rerank_documents
from langchain.schema import AIMessage

import numpy as np

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM



def get_memory():
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=4
    )


# def cosine_similarity(vec1, vec2):
#     """
#     Calcula la similitud coseno entre dos vectores.
#     """
#     vec1 = np.array(vec1)
#     vec2 = np.array(vec2)
#     return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# def rag_chain_con_umbral(rag_chain, question, threshold=0.8):
#     """
#     Aplica umbral de confianza antes de invocar el chain.
#     Si no hay score en metadata, calcula la similitud manualmente.
#     """
#     retriever = rag_chain.retriever
#     vectorstore = retriever.vectorstore
#     embedder = vectorstore.embedding_function

#     # Obtener vector de la pregunta
#     question_vector = embedder.embed_query(question)

#     docs = retriever.get_relevant_documents(question)

#     print(" Documentos recuperados y sus scores:")
#     for i, doc in enumerate(docs, 1):
#         score = doc.metadata.get("score", None)
#         if score is None:
#             # Calcular la similitud manualmente
#             chunk_vector = embedder.embed_query(doc.page_content)
#             score = cosine_similarity(question_vector, chunk_vector)
#             print(f"   {i}. (Calculado) Score: {score:.4f} | Source: {doc.metadata.get('source')}")
#         else:
#             print(f"   {i}. (FAISS) Score: {score:.4f} | Source: {doc.metadata.get('source')}")
#         doc.metadata["score"] = score  # Guarda el score en metadata por si se usa luego

#     similitud = docs[0].metadata["score"]

#     print(f"Similitud máxima: {similitud:.4f}")

#     if similitud < threshold:
#         print(f" Similitud ({similitud:.4f}) < threshold ({threshold}), devolviendo respuesta fallback.")
#         respuesta = (
#             "No se ha encontrado una respuesta clara en la normativa. "
#             "Te recomendamos contactar con la Unidad de Prácticas en Empresa (upe_inf@etsinf.upv.es)."
#         )
#         return {"answer": respuesta, "source_documents": []}
#     else:
#         return rag_chain({"question": question})


# def crear_rag_chain(vectorstore, memory, custom_prompt, role: str):
#     """
#     Crea una cadena RAG para el rol dado ("estudiante" o "empresa").
#     Filtra los documentos por metadata['role'] antes de la recuperación.
#     """
#     llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

#     retriever = vectorstore.as_retriever(
#         search_type="mmr",
#         search_kwargs={
#             "k": 15,
#             "fetch_k": 40,
#             "lambda_mult": 0.5,
#             "filter": {"role": role},
#             "score":True
#         }
#     )

#     rag_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=retriever,
#         memory=memory,
#         return_source_documents=True,
#         output_key="answer",
#         combine_docs_chain_kwargs={"prompt": custom_prompt}
#     )
#     return rag_chain



# Cargar modelo y tokenizer
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")

def reformular_respuesta_local(respuesta_original, role):
    """
    Reformula una respuesta usando bart-base.
    """
    prompt = f"Reformula el siguiente texto para que sea claro, directo y profesional (dirigido a {role}). No añadas datos nuevos:\n\n{respuesta_original}"
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

    # Generar la reformulación
    outputs = model.generate(**inputs, max_length=512, num_beams=4, early_stopping=True)
    reformulada = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reformulada.strip()


def crear_rag_chain(vectorstore, memory, custom_prompt, role: str):
    """
    Crea una cadena RAG para el rol dado ("estudiante" o "empresa").
    Filtra los documentos por metadata['role'] antes de la recuperación.
    Aplica un reranker para mejorar la calidad de los chunks recuperados.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    reranker_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
    
    compressor = CrossEncoderReranker(model=reranker_model, top_n=15)

    base_retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 12,
            "fetch_k": 50,
            "lambda_mult": 0.5,
            "filter": {"role": role},
            "score": True
        }
    )
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever
    )

    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=compression_retriever,
        memory=memory,
        return_source_documents=True,
        output_key="answer",
        combine_docs_chain_kwargs={"prompt": custom_prompt}
    )
    return rag_chain

# def filtrar_por_confianza(docs, threshold=0.7):
#     """
#     Comprueba la similitud del mejor chunk.
#     Si es menor que el umbral, devuelve None.
#     """
#     if not docs:
#         return None

#     # Recupera el score del mejor chunk
#     similitud = docs[0].metadata.get("score", 1.0)
#     print(f"🔍 Similitud máxima: {similitud:.2f}")

#     if similitud < threshold:
#         return None
#     return docs


# def filtrar_por_confianza(docs, threshold=0.7):
#     """
#     Comprueba la similitud del mejor chunk.
#     Si es menor que el umbral, devuelve None.
#     """
#     if not docs:
#         print(" No se han recuperado documentos.")
#         return None

#     print(" Documentos recuperados y sus scores:")
#     for i, doc in enumerate(docs, 1):
#         score = doc.metadata.get("score", None)
#         print(f"   {i}. Score: {score} | Source: {doc.metadata.get('source')}")

#     # Recupera el score del mejor chunk
#     similitud = docs[0].metadata.get("score", None)
#     if similitud is None:
#         print(" No se encontró 'score' en metadata. ¿Seguro que retriever tiene score=True?")
#         similitud = 1.0  # Asume confianza máxima por defecto

#     print(f" Similitud máxima: {similitud:.2f}")

#     if similitud < threshold:
#         print(f" Similitud ({similitud:.2f}) < threshold ({threshold}), descartando resultados.")
#         return None
#     return docs



# def crear_rag_chain_con_reranker(vectorstore, memory, custom_prompt, use_reranker=False):
#     llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
#     retriever = vectorstore.as_retriever(
#         search_type="mmr",
#         search_kwargs={"k": 15, "fetch_k": 40, "lambda_mult": 0.3}
#     )

#     def custom_retrieval_func(inputs):
#         question = inputs["question"]
#         initial_docs = retriever.get_relevant_documents(question)
#         if use_reranker:
#             return rerank_documents(question, initial_docs, top_k=6)
#         return initial_docs


#     rag_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=retriever,
#         memory=memory,
#         return_source_documents=True,
#         output_key="answer",
#         combine_docs_chain_kwargs={"prompt": custom_prompt}
#     )
#     rag_chain.retriever.get_relevant_documents = custom_retrieval_func  # override

#     return rag_chain



# def recuperar_y_rerankear(query, retriever, usar_reranker=True, top_k=8):
#     docs = retriever.get_relevant_documents(query)
#     if usar_reranker:
#         return rerank_documents(query, docs, top_k=top_k)
#     return docs

# def generar_respuesta(llm, prompt_template, question, context_docs, chat_history):
#     context = "\n\n".join([doc.page_content for doc in context_docs])
#     chat_formateado = "\n".join([f"{r.upper()}: {m}" for r, m in chat_history])
#     prompt = prompt_template.format(
#         question=question,
#         context=context,
#         chat_history=chat_formateado
#     )
#     return llm([AIMessage(content=prompt)]).content
