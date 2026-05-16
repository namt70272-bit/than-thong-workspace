# C: Drive Analysis — 341 GB / 476 GB (71.6%)

## BIGGEST SPACE USERS

### 1. WSL (Windows Subsystem Linux) — ~11.5 GB
- Ubuntu + Ubuntu-24.04 + docker-desktop
- ✅ Useful if actively using Linux
- ⚠️ Chiếm nhiều, có thể nén/distro export sang E:

### 2. npm cache — ~4.8 GB 
- `C:\Users\ACER\AppData\Local\npm-cache`
- ❌ CHIẾM NHIỀU NHẤT — có thể xóa an toàn
- `npm cache clean --force` → giải phóng ~5 GB

### 3. Ollama models — ~4.5 GB
- `C:\Users\ACER\.ollama\models\blobs` (4,466 MB)
- ✅ Có ích, nhưng nên chuyển sang E: hoặc D:

### 4. Program Files — ~13 GB
- Blackmagic Design: lớn nhất (driver/software video)
- ⚠️ Kiểm tra có cần không

### 5. WinSxS — ~10 GB
- Windows component store
- ⚠️ Có thể dọn bằng `DISM.exe /Online /Cleanup-Image /StartComponentCleanup`

### 6. Windows System32 — ~8 GB
- DriverStore lớn nhất
- Có thể dọn driver cũ

### 7. AppData Local (còn lại) — ~38 GB
- WSL: 11.5 GB
- Các updater (ac-electron, obsidian, canva, notion...)
- Pip cache: 722 MB
- Temp: 240 MB

### 8. pip cache — 722 MB
- `C:\Users\ACER\AppData\Local\pip`
- `pip cache purge` → giải phóng ~700 MB

### 9. AppData Roaming — ~2.7 GB
- ZaloData: 676 MB
- Movavi: 408 MB
- Zoom: 176 MB
- Telegram: 128 MB
- VS Code: 74 MB

## SUMMARY TABLE

| Item | Size | Có thể dọn? | Tiết kiệm |
|------|------|-------------|-----------|
| npm cache | 4.8 GB | ✅ An toàn | ~5 GB |
| pip cache | 722 MB | ✅ An toàn | ~0.7 GB |
| Temp files | 240 MB | ✅ An toàn | ~0.2 GB |
| WinSxS cleanup | ~10 GB | ⚠️ Thận trọng | ~3-5 GB |
| WSL export → E: | 11.5 GB | ✅ Nếu không dùng thường xuyên | ~11 GB |
| Ollama → E: | 4.5 GB | ✅ Nên chuyển | ~4.5 GB |
| Windows.old | 0 GB | ✅ (không có) | 0 GB |
| **TOTAL TIẾT KIỆM** | | | **~20 GB** |

## ESTIMATE SAU KHI DỌN

| Ổ | Hiện tại | Sau dọn | Target |
|---|----------|---------|--------|
| C: | 341 GB / 476 GB (71.6%) | ~320 GB (67%) | < 300 GB |
| E: | 269 GB / 932 GB (28.9%) | ~285 GB (30%) | < 300 GB |
