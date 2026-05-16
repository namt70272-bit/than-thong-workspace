#!/usr/bin/env python3
"""
Web Search module for OpenClaw agent
Primary: FireCrawl (API key needed)
Fallback: httpx direct fetch
"""
import os, json, sys
from datetime import datetime

SEARCH_DIR = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal\agent-search"
os.makedirs(SEARCH_DIR, exist_ok=True)

# Try FireCrawl
FIRECRAWL_AVAILABLE = False
firecrawl_app = None
try:
    from firecrawl import FirecrawlApp
    api_key = os.environ.get("FIRECRAWL_API_KEY", "")
    if api_key:
        firecrawl_app = FirecrawlApp(api_key=api_key)
        FIRECRAWL_AVAILABLE = True
except Exception:
    pass

# Always try basic fetch
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

def web_search(query: str, limit: int = 5):
    """Search web using FireCrawl or fallback"""
    result = {"query": query, "results": [], "source": ""}
    
    # Mode 1: FireCrawl
    if FIRECRAWL_AVAILABLE and firecrawl_app:
        try:
            crawl = firecrawl_app.search(query=query, params={"count": limit})
            result["source"] = "firecrawl"
            for item in crawl.get("results", []) or crawl.get("data", []):
                result["results"].append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "description": item.get("description", "") or item.get("content", "")[:200],
                })
            return result
        except Exception as e:
            result["firecrawl_error"] = str(e)
    
    # Mode 2: Basic httpx search via Brave/DuckDuckGo
    if HTTPX_AVAILABLE:
        try:
            resp = httpx.get(
                f"https://lite.duckduckgo.com/lite/?q={query}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            result["source"] = "httpx"
            result["status_code"] = resp.status_code
            result["raw_preview"] = resp.text[:1000]
            return result
        except Exception as e:
            result["http_error"] = str(e)
    
    result["source"] = "none"
    result["error"] = "No search engine available"
    return result

def fetch_url(url: str):
    """Fetch a URL and return text content"""
    if HTTPX_AVAILABLE:
        try:
            resp = httpx.get(url, timeout=15, follow_redirects=True)
            return {"url": url, "status": resp.status_code, "content": resp.text[:10000]}
        except Exception as e:
            return {"url": url, "error": str(e)}
    return {"url": url, "error": "httpx not available"}

if __name__ == "__main__":
    print("Web Search Module")
    print(f"  FireCrawl: {'AVAILABLE' if FIRECRAWL_AVAILABLE else 'NEED API KEY'}")
    print(f"  httpx fallback: {'YES' if HTTPX_AVAILABLE else 'NO'}")
    
    # Quick test
    if len(sys.argv) > 1:
        q = sys.argv[1]
        print(f"\nSearch: '{q}'")
        r = web_search(q)
        print(f"  Source: {r['source']}")
        for item in r.get("results", [])[:3]:
            print(f"  - {item.get('title', 'N/A')}: {item.get('url', 'N/A')}")
