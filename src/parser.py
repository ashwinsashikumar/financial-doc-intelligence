import pdfplumber

def extract_structured_documents(pdf_path, max_pages=15):
    """
    Extracts narrative text and detects tables, formatting tables
    into clean Markdown schema with page-level metadata.
    """
    documents = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages[:max_pages]):
            page_num = page_idx + 1
            
            # Extract Tables
            tables = page.extract_tables()
            for table_idx, table in enumerate(tables):
                cleaned_rows = []
                for row in table:
                    cleaned_row = [str(c).strip().replace("\n", " ") if c is not None else "" for c in row]
                    if any(cleaned_row):
                        cleaned_rows.append(cleaned_row)
                
                if len(cleaned_rows) > 1:
                    headers = cleaned_rows[0]
                    separator = ["---"] * len(headers)
                    md_table_rows = ["| " + " | ".join(headers) + " |", "| " + " | ".join(separator) + " |"]
                    for r in cleaned_rows[1:]:
                        md_table_rows.append("| " + " | ".join(r) + " |")
                    
                    documents.append({
                        "content": "\n".join(md_table_rows),
                        "metadata": {"page": page_num, "type": "table", "item_id": f"p{page_num}_t{table_idx+1}"}
                    })
            
            # Extract Narrative
            text = page.extract_text()
            if text:
                paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 60]
                for p_idx, para in enumerate(paragraphs):
                    documents.append({
                        "content": para.replace("\n", " "),
                        "metadata": {"page": page_num, "type": "narrative", "item_id": f"p{page_num}_p{p_idx+1}"}
                    })
    return documents
