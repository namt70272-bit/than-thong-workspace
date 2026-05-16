import sys, time, base64
from playwright.sync_api import sync_playwright

def open_url(url, headless=False, wait_sec=0):
    """Mở URL bằng Playwright Chromium, giữ browser sống."""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    
    try:
        page.goto(url, timeout=30000)
        title = page.title()
        print(f"TITLE: {title}", flush=True)
        print(f"URL: {page.url}", flush=True)
        
        if wait_sec > 0:
            print(f"WAIT: {wait_sec}s", flush=True)
            time.sleep(wait_sec)
        
        # Screenshot
        ss = page.screenshot()
        print(f"SCREENSHOT: {base64.b64encode(ss).decode()[:50]}...", flush=True)
        
        # Elements
        for i, el in enumerate(page.locator("button, a, input, [role=button]").all()[:30]):
            text = (el.inner_text() or "")[:60]
            tag = el.evaluate("el => el.tagName.toLowerCase()")
            if text.strip():
                vis = "✓" if el.is_visible() else "✗"
                print(f"  [{i}] <{tag}> {text.strip()} [{vis}]", flush=True)
        
        # Giữ browser mở — user tự close
        print("READY: Browser is open. Close the Chrome window when done.", flush=True)
        while True:
            try:
                # Kiểm tra browser còn sống không
                page.title()
                time.sleep(2)
            except:
                print("Browser closed.", flush=True)
                break
    finally:
        browser.close()
        p.stop()

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    wait = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    headless = "--headless" in sys.argv
    open_url(url, headless=headless, wait_sec=wait)
