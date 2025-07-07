from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from reranker import rerank_documents
from langchain.schema import AIMessage


def get_memory():
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
        k=5
    )


def crear_rag_chain(vectorstore, memory, custom_prompt, role: str):
    """
    Crea una cadena RAG para el rol dado ("estudiante" o "empresa").
    Filtra los documentos por metadata['role'] antes de la recuperación.
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 10,
            "fetch_k": 30,
            "lambda_mult": 0.3,
            "filter": {"role": role}
        }
    )

    rag_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        output_key="answer",
        combine_docs_chain_kwargs={"prompt": custom_prompt}
    )
    return rag_chain




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
