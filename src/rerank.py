import re

def compute_relevance_score(query, doc_content):
    query_terms = set(re.findall(r'\w+', query.lower()))
    content_terms = re.findall(r'\w+', doc_content.lower())
    if not content_terms:
        return 0.0
    matched_terms = [t for t in content_terms if t in query_terms]
    term_density = len(matched_terms) / len(content_terms)
    coverage = len(set(matched_terms)) / (len(query_terms) + 1e-6)
    table_boost = 1.25 if ("|" in doc_content and bool(re.search(r'\d+', doc_content))) else 1.0
    return (coverage * 0.7 + term_density * 0.3) * table_boost

def rerank_candidates(query, candidates, top_k=3):
    scored = [{**c, "rerank_score": compute_relevance_score(query, c["doc"]["content"])} for c in candidates]
    return sorted(scored, key=lambda x: x["rerank_score"], reverse=True)[:top_k]
