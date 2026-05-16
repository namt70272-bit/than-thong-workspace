# Than Thong — Cong Kiem Soat May Tinh

Ung dung desktop: cong (gate) + dinh tuyen (router) + system tray + cong cu Windows.
**File .exe doc lap** — khong can Python.

## Cach dung

```
than-thong.exe                    # App system tray (mac dinh)
than-thong.exe console            # Dieu khien tuong tac
than-thong.exe dieu-khien         # (tieng Viet)
than-thong.exe kiem-tra-cong      # Kiem tra cong
than-thong.exe trang-thai         # Trang thai he thong
than-thong.exe thong-tin          # Thong tin may tinh
than-thong.exe don-dep            # Don file tam
than-thong.exe kiem-tra-bao-mat   # Kiem tra bao mat

# English (tuong thich nguoc)
than-thong.exe gate-test
than-thong.exe status
than-thong.exe info
than-thong.exe win-cleanup
than-thong.exe win-audit
```

## Windows SmartScreen / Windows Defender

Ung dung duoc xay dung bang PyInstaller va **khong co chu ky so**.  
Windows co the canh bao "Windows protected your PC" lan dau chay.

**Tai sao:** Giay phep ky so gia $200-400/nam.  
**An toan:** Ma nguon mo, MIT license, khong truy cap mang.

### Cach chay:

1. Nhan **"More info"** (hoac "Thong tin them")
2. Nhan **"Run anyway"** (hoac "Chay van")
3. App chay — cong kiem soat hoat dong

### Windows Defender:

Neu Defender cach ly file .exe, them ngoai le:
```
Windows Security → Virus & threat protection →
Manage settings → Exclusions → Add exclusion → File
```

## Giao dien

System tray:
- **Trang thai** — Xem engine
- **Kiem tra cong** — Kiem tra chinh sach
- **Don dep Windows** — Don file tam 1 click
- **Mo dieu khien** — Mo terminal
- **Cai dat** — Thong bao, auto-start, cau hinh
- **Thoat** — Thoat ung dung

## Gia Content

Xem file `LICENSE`.

## Tu source

```powershell
pip install -r requirements.txt
pip install pyinstaller
python build.py
```
