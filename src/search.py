import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

class HybridSearchEngine:
    def __init__(self, documents):
        self.documents = documents
        self.corpus = [d["content"] for d in documents]
        
        # Dense Vector Space
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words='english')
        self.dense_matrix = self.vectorizer.fit_transform(self.corpus)
        
        # Sparse BM25
        self.tokenized_corpus = [d["content"].lower().split() for d in documents]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def search(self, query, top_k=5, rrf_k=60):
        # Dense Retrieval
        q_vec = self.vectorizer.transform([query])
        dense_scores = cosine_similarity(q_vec, self.dense_matrix).flatten()
        dense_ranked = np.argsort(dense_scores)[::-1]

        # BM25 Retrieval
        q_tokens = query.lower().split()
        bm25_scores = np.array(self.bm25.get_scores(q_tokens))
        sparse_ranked = np.argsort(bm25_scores)[::-1]

        # Reciprocal Rank Fusion
        rrf_scores = {}
        for rank, idx in enumerate(dense_ranked[:top_k * 3]):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (1.0 / (rrf_k + (rank + 1)))
        for rank, idx in enumerate(sparse_ranked[:top_k * 3]):
            rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (1.0 / (rrf_k + (rank + 1)))

        sorted_ids = sorted(rrf_scores.keys(), key=lambda i: rrf_scores[i], reverse=True)[:top_k]
        return [{
            "doc": self.documents[i],
            "rrf_score": rrf_scores[i],
            "dense_score": float(dense_scores[i]),
            "bm25_score": float(bm25_scores[i])
        } for i in sorted_ids]
