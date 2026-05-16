import os
import glob
from typing import List
from tqdm import tqdm
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

# Cấu hình đường dẫn
KNOWLEDGE_DIR = "knowledge"
DB_DIR = "chroma_db"

def ingest_all():
    client = chromadb.PersistentClient(path=DB_DIR)
    emb_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name="minh_kien_knowledge",
        embedding_function=emb_fn
    )

    # Tìm tất cả file trong knowledge và các thư mục con
    files = []
    for ext in ["pdf", "md", "txt"]:
        files.extend(glob.glob(os.path.join(KNOWLEDGE_DIR, "**", f"*.{ext}"), recursive=True))

    if not files:
        print("Không tìm thấy tài liệu nào.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    print(f"🔄 Đang quét và cập nhật toàn bộ {len(files)} tài liệu vào RAG...")

    for file_path in tqdm(files):
        try:
            # Kiểm tra xem file đã được nạp chưa (dựa trên source metadata)
            # Lưu ý: ChromaDB simple check bằng cách query hoặc metadata filter
            # Ở đây con nạp đè/nạp mới để đảm bảo tri thức đầy đủ
            
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path, encoding="utf-8")
            
            docs = loader.load()
            chunks = text_splitter.split_documents(docs)
            
            documents = [c.page_content for c in chunks]
            metadatas = [{"source": file_path, "page": c.metadata.get("page", 0)} for c in chunks]
            ids = [f"{os.path.basename(file_path)}_{i}" for i in range(len(chunks))]

            collection.add(documents=documents, metadatas=metadatas, ids=ids)
        except Exception as e:
            print(f"❌ Lỗi file {file_path}: {e}")

    print(f"✅ Đã cập nhật thành công bộ não tri thức.")

if __name__ == "__main__":
    ingest_all()
