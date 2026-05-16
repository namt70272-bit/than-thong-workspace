import os
import chromadb
from chromadb.utils import embedding_functions

# Cấu hình đường dẫn
DB_DIR = "chroma_db"

def query_brain(query_text: str, n_results: int = 3):
    # 1. Kết nối ChromaDB
    client = chromadb.PersistentClient(path=DB_DIR)
    
    # Sử dụng mô hình embedding mặc định
    emb_fn = embedding_functions.DefaultEmbeddingFunction()
    
    # Lấy collection
    try:
        collection = client.get_collection(
            name="minh_kien_knowledge",
            embedding_function=emb_fn
        )
    except Exception:
        print("Lỗi: 'Bộ não' chưa được khởi tạo. Vui lòng chạy ingest.py trước.")
        return

    # 2. Truy vấn
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )

    # 3. Hiển thị kết quả
    print(f"\n--- Kết quả truy vấn cho: '{query_text}' ---")
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        print(f"\n[{i+1}] Nguồn: {meta.get('source', 'Unknown')} (Trang: {meta.get('page', 'N/A')})")
        print(f"Nội dung: {doc[:300]}...")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query_brain(sys.argv[1])
    else:
        q = input("Nhập câu hỏi của Thầy: ")
        query_brain(q)
