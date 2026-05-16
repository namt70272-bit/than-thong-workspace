import sys, time, urllib.parse
from playwright.sync_api import sync_playwright

query = "Vang Trang Khuyet Tung Duong"
url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    page.goto(url, timeout=30000)
    sys.stdout.write("Da mo YouTube...\n")
    sys.stdout.flush()
    time.sleep(3)
    
    videos = page.locator("a#video-title").all()
    if videos:
        title = videos[0].get_attribute("title") or "Unknown"
        sys.stdout.write("Dang phat: " + title + "\n")
        sys.stdout.flush()
        videos[0].click()
        time.sleep(3)
    
    sys.stdout.write("Nhac dang phat! Dong tab Chrome khi muon dung.\n")
    sys.stdout.flush()
    
    try:
        while True:
            page.title()
            time.sleep(2)
    except:
        pass
    browser.close()
