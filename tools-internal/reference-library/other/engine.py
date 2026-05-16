import os
import httpx
from bs4 import BeautifulSoup
import trafilatura
from markdownify import markdownify as md
from urllib.parse import urlparse

class WebScraper:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def scrape(self, url):
        print(f"Đang cào dữ liệu từ: {url}")
        try:
            # Thử lấy nội dung bằng trafilatura (tối ưu cho bài báo/blog)
            downloaded = trafilatura.fetch_url(url)
            result = trafilatura.extract(downloaded, include_links=True, include_images=True)
            
            if not result:
                # Nếu trafilatura thất bại, dùng httpx + BeautifulSoup làm fallback
                response = httpx.get(url, follow_redirects=True, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                result = md(str(soup))

            return result
        except Exception as e:
            return f"Lỗi khi cào dữ liệu: {str(e)}"

    def save_to_markdown(self, url, content):
        domain = urlparse(url).netloc.replace('.', '_')
        path = urlparse(url).path.replace('/', '_')
        if path == "_": path = "_index"
        filename = f"{domain}{path}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"--- \nsource: {url}\n---\n\n")
            f.write(content)
        
        return filepath

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        scraper = WebScraper()
        content = scraper.scrape(url)
        path = scraper.save_to_markdown(url, content)
        print(f"Đã lưu nội dung vào: {path}")
