from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")

def rerank_documents(query, documents, top_k=8):
    pairs = [(query, doc.page_content) for doc in documents]
    scores = reranker.predict(pairs)
    scored_docs = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored_docs[:top_k]]
