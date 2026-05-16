import os
import shutil
import sys

# Đường dẫn nguồn và đích
SCRAPER_OUTPUT = "/home/hgahc/.openclaw/workspace/projects/web-tools/scraper/output"
RAG_KNOWLEDGE = "/home/hgahc/.openclaw/workspace/projects/rag-system/knowledge"

def sync_to_rag(filename=None):
    if not os.path.exists(RAG_KNOWLEDGE):
        os.makedirs(RAG_KNOWLEDGE)
        
    if filename:
        src_path = os.path.join(SCRAPER_OUTPUT, filename)
        if os.path.exists(src_path):
            shutil.copy(src_path, RAG_KNOWLEDGE)
            print(f"KẾT QUẢ: Đã nạp thành công '{filename}' vào bộ nhớ RAG.")
            return True
        else:
            print(f"LỖI: Không tìm thấy file '{filename}' trong output của scraper.")
            return False
    else:
        # Nếu không chỉ định file, nạp toàn bộ file mới
        files = [f for f in os.listdir(SCRAPER_OUTPUT) if f.endswith('.md')]
        for f in files:
            shutil.copy(os.path.join(SCRAPER_OUTPUT, f), RAG_KNOWLEDGE)
        print(f"KẾT QUẢ: Đã đồng bộ toàn bộ {len(files)} tài liệu vào bộ nhớ RAG.")
        return True

if __name__ == "__main__":
    file_arg = sys.argv[1] if len(sys.argv) > 1 else None
    sync_to_rag(file_arg)
