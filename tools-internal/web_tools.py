#!/usr/bin/env python
"""
Enhanced Web Tools — scraping + data extraction
Reference: web-scraping/ (youtube_downloader, edgar_fetcher patterns)
"""
import os, sys, json, httpx, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

class WebTools:
    
    @staticmethod
    def extract_links(html):
        """Extract all links from HTML"""
        pattern = re.compile(r'href=[\'"]?([^\'" >]+)')
        return pattern.findall(html)
    
    @staticmethod
    def extract_text(html):
        """Extract text from HTML (strip tags)"""
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()[:5000]
    
    @staticmethod
    def search_duckduckgo(query, limit=5):
        """Search via DuckDuckGo HTML (free, no API key)"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={query}"
            r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            html = r.text
            # Extract results
            results = []
            for match in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.DOTALL):
                if len(results) >= limit:
                    break
                url = match.group(1)
                title = re.sub(r'<[^>]+>', '', match.group(2)).strip()
                results.append({"title": title, "url": url})
            return results
        except Exception as e:
            return [{"error": str(e)[:80]}]
    
    @staticmethod
    def fetch_page_text(url):
        """Fetch a page and extract clean text"""
        try:
            r = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15, follow_redirects=True)
            text = WebTools.extract_text(r.text)
            return {"url": url, "status": r.status_code, "content": text[:5000]}
        except Exception as e:
            return {"error": str(e)[:80]}

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if action == "search":
        q = " ".join(sys.argv[2:])
        results = WebTools.search_duckduckgo(q)
        for r in results:
            print(f"  {r.get('title', '?')}")
            print(f"    {r.get('url', '?')}")
    elif action == "fetch":
        url = sys.argv[2] if len(sys.argv) > 2 else "https://example.com"
        result = WebTools.fetch_page_text(url)
        print(f"Status: {result.get('status')}")
        print(f"Content: {result.get('content', '')[:300]}")
    else:
        print("Web Tools (DuckDuckGo fallback)")
        print("  search <query>  - Search web")
        print("  fetch  <url>    - Fetch page text")
