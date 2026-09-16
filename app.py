import argparse
from src.parser import extract_structured_documents
from src.search import HybridSearchEngine
from src.rerank import rerank_candidates
from src.synthesis import generate_audit_answer

def run_audit(pdf_path, query):
    print(f"[*] Ingesting and parsing {pdf_path}...")
    docs = extract_structured_documents(pdf_path)
    engine = HybridSearchEngine(docs)
    
    print(f"[*] Executing Hybrid Search (Dense + BM25 with RRF)...")
    candidates = engine.search(query, top_k=6)
    
    print(f"[*] Re-ranking via cross-scoring layer...")
    ranked = rerank_candidates(query, candidates, top_k=2)
    
    print(f"[*] Synthesizing audited memo...")
    res = generate_audit_answer(query, ranked)
    print("\n" + res["memo"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audited Document Intelligence Engine")
    parser.add_argument("--pdf", type=str, default="financial_report.pdf", help="Target PDF file")
    parser.add_argument("--query", type=str, required=True, help="Audit verification query")
    args = parser.parse_args()
    run_audit(args.pdf, args.query)
