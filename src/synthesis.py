def generate_audit_answer(query, top_docs):
    if not top_docs or top_docs[0]["rerank_score"] < 0.05:
        return {"status": "REFUSED", "memo": "INSUFFICIENT EVIDENCE: No disclosures found matching criteria."}
    
    citations, evidence_blocks = [], []
    for item in top_docs:
        meta = item["doc"]["metadata"]
        ref = f"[Page {meta['page']} | {meta['type'].upper()} ({meta['item_id']})]"
        citations.append(ref)
        evidence_blocks.append(f"Source {ref}:\n{item['doc']['content'].strip()}")
    
    memo = f"""=== AUDIT COMPLIANCE MEMO ===\nQUERY: {query}\n\nKEY EXTRACTED DISCLOSURES:\n{'\n\n'.join(evidence_blocks)}\n\nAUDIT CITATIONS:\n- Verified across: {', '.join(citations)}\n============================="""
    return {"status": "VERIFIED", "memo": memo, "citations": citations}
