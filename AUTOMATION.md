# AUTOMATION.md — Luật Điều Phối Tự Động

> Tôi là automation orchestrator, không phải người click chuột.

## Thứ tự ưu tiên (bắt buộc theo đúng thứ tự)

| # | Tình huống | Phương án |
|---|---|---|
| 1 | Có API / CLI / script | Dùng API/CLI/script |
| 2 | Web app | Playwright |
| 3 | File / media | Python / Node / FFmpeg xử lý trực tiếp |
| 4 | Desktop app có UI tree | Power Automate / pywinauto / AutoHotkey |
| 5 | Không còn cách khác | Screenshot + tọa độ chuột (last resort) |

## Luật vận hành

- **Hotkey trước click:** Không click từng bước nếu có hotkey tương đương.
- **Không scan liên tục:** Chỉ screenshot vùng cần kiểm tra, không quét toàn màn hình.
- **Ghi nhớ sau lần đầu:** Workflow, tọa độ, hotkey, template → lưu vào file để tái sử dụng.
- **Script reusable:** Tác vụ lặp lại → tạo script trước, sau đó chỉ gọi script.
- **Xác nhận bắt buộc:** Mọi thao tác nguy hiểm (xóa file, gửi email, thanh toán, đăng bài public) phải hỏi trước khi thực thi.

## Stack hiện có (đã kiểm tra)

| Tool | Loại | Version | Dùng cho |
|---|---|---|---|
| ffmpeg | CLI | 8.1 | Encode/render video, audio |
| ImageMagick | CLI | 7.1.2 | Xử lý ảnh, composite, text overlay |
| moviepy | Python | 2.2.1 | Video pipeline trong Python |
| Pillow | Python | 11.3.0 | Ảnh, crop, resize, text |
| OpenCV | Python | 4.13.0 | Computer vision, template matching |
| numpy | Python | 2.4.4 | Array/matrix ops |
| imageio | Python | 2.37.3 | Đọc/ghi frame video |
| Jinja2 | Python | 3.1.6 | Template rendering |
| Playwright | Python | 1.59.0 | Web automation (CapCut web, v.v.) |
| pywinauto | Python | 0.6.9 | Desktop app UI tree |
| pyautogui | Python | 0.9.54 | Mouse/keyboard (last resort) |
| win32gui/api | Python | - | Window focus, HWND |
| rich | Python | 15.0.0 | Terminal output |
| typer | Python | 0.24.1 | CLI script builder |

## Workflow: Video quảng cáo từ ảnh

**Pipeline chuẩn (không cần CapCut):**
```
ảnh input → Pillow/ImageMagick (resize, overlay text, logo)
          → FFmpeg (ken burns / zoom effect, nhạc nền, subtitle)
          → output .mp4
```

**Script template:** `scripts/ad_video/make_ad.py`

---

_Cập nhật: 2026-05-12_
