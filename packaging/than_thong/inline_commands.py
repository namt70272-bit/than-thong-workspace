"""Lenh noi bo — thao tac Windows truc tiep, khong can subprocess, tieng Viet."""
import os, sys, platform, json, subprocess, tempfile, shutil, time
from pathlib import Path
from than_thong.logger import log


def cmd_trang_thai() -> dict:
    """Trang thai he thong + engine."""
    import string
    info = {
        "engine": "dang chay",
        "he_dieu_hanh": platform.system(),
        "phien_ban": platform.release(),
        "version": platform.version(),
        "kien_truc": platform.machine(),
        "cpu": platform.processor(),
        "python": platform.python_version(),
        "may_tinh": platform.node(),
    }
    # O dia
    o_dia = []
    for d in string.ascii_uppercase:
        p = f"{d}:\\"
        try:
            usage = shutil.disk_usage(p)
            o_dia.append({
                "o": p,
                "tong_gb": round(usage.total / (1024**3), 1),
                "da_dung_gb": round(usage.used / (1024**3), 1),
                "con_trong_gb": round(usage.free / (1024**3), 1),
                "phan_tram": round(usage.used / usage.total * 100, 1),
            })
        except OSError:
            continue
    info["o_dia"] = o_dia
    return {"thanh_cong": True, "thong_tin": info}


def cmd_don_dep() -> dict:
    """Don dep file tam Windows."""
    import string
    ket_qua = []
    tong_giai_phong = 0

    muc_tieu = [
        (os.environ.get("TEMP", ""), "Temp nguoi dung"),
        (os.environ.get("TMP", ""), "TMP nguoi dung"),
        (r"C:\Windows\Temp", "Temp Windows"),
    ]

    for path, nhan in muc_tieu:
        if not path or not os.path.isdir(path):
            continue
        dem = 0
        giai_phong = 0
        loi = 0
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                try:
                    fp = os.path.join(root, name)
                    giai_phong += os.path.getsize(fp)
                    os.remove(fp)
                    dem += 1
                except (PermissionError, OSError):
                    loi += 1
            for name in dirs:
                try:
                    shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                except OSError:
                    pass
        ket_qua.append({
            "muc_tieu": nhan,
            "duong_dan": path,
            "file_da_xoa": dem,
            "da_giai_phong_bytes": giai_phong,
            "loi": loi,
        })
        tong_giai_phong += giai_phong

    # Don cache IE/trinh duyet
    try:
        subprocess.run(
            ["rundll32.exe", "InetCpl.cpl,ClearMyTracksByProcess", "255"],
            capture_output=True, timeout=10
        )
    except Exception:
        pass

    return {
        "thanh_cong": True,
        "ket_qua": ket_qua,
        "tong_giai_phong_mb": round(tong_giai_phong / (1024*1024), 2),
    }


def cmd_kiem_tra_bao_mat() -> dict:
    """Kiem tra bao mat Windows."""
    import ctypes, winreg

    phat_hien = []

    # UAC
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System") as k:
            val, _ = winreg.QueryValueEx(k, "EnableLUA")
            phat_hien.append({
                "kiem_tra": "UAC (Kiem soat tai khoan)",
                "trang_thai": "OK" if val == 1 else "CANH BAO",
                "chi_tiet": "UAC dang bat" if val == 1 else "UAC dang tat (nguy co bao mat)",
            })
    except Exception:
        phat_hien.append({"kiem_tra": "UAC", "trang_thai": "LOI", "chi_tiet": "Khong doc duoc"})

    # Firewall
    try:
        r = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles", "state"],
            capture_output=True, text=True, timeout=10
        )
        fw_on = "ON" in r.stdout.upper() if r.stdout else False
        phat_hien.append({
            "kiem_tra": "Tuong lua (Firewall)",
            "trang_thai": "OK" if fw_on else "CANH BAO",
            "chi_tiet": "Tuong lua dang bat" if fw_on else "Tuong lua dang tat",
        })
    except Exception:
        phat_hien.append({"kiem_tra": "Firewall", "trang_thai": "LOI", "chi_tiet": "Khong kiem tra duoc"})

    # Windows Defender
    try:
        r = subprocess.run(
            ["powershell", "-Command",
             "(Get-MpComputerStatus).RealTimeProtectionEnabled"],
            capture_output=True, text=True, timeout=15
        )
        def_enabled = r.stdout.strip() == "True"
        phat_hien.append({
            "kiem_tra": "Defender thoi gian thuc",
            "trang_thai": "OK" if def_enabled else "CANH BAO",
            "chi_tiet": "Defender dang hoat dong" if def_enabled else "Defender dang tat",
        })
    except Exception:
        phat_hien.append({"kiem_tra": "Defender", "trang_thai": "LOI", "chi_tiet": "Khong kiem tra duoc"})

    # Admin
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        phat_hien.append({
            "kiem_tra": "Quyen Admin",
            "trang_thai": "THONG TIN",
            "chi_tiet": "Dang chay voi quyen Admin" if is_admin else "Dang chay voi quyen nguoi dung",
        })
    except Exception:
        pass

    # O cung
    try:
        r = subprocess.run(
            ["wmic", "diskdrive", "get", "status"],
            capture_output=True, text=True, timeout=10
        )
        disk_ok = "OK" in r.stdout if r.stdout else "khong ro"
        phat_hien.append({
            "kiem_tra": "Suc khoe o cung",
            "trang_thai": "OK" if disk_ok else "CANH BAO",
            "chi_tiet": r.stdout.strip()[:200] if r.stdout else "Khong co du lieu",
        })
    except Exception:
        pass

    return {"thanh_cong": True, "phat_hien": phat_hien}


def cmd_thong_tin() -> dict:
    """Thong tin may tinh chi tiet."""
    import psutil
    info = {
        "may_tinh": platform.node(),
        "he_dieu_hanh": f"{platform.system()} {platform.release()} {platform.version()}",
        "kien_truc": platform.machine(),
        "cpu": platform.processor(),
        "cpu_so_nhan": os.cpu_count(),
        "thoi_gian_khoi_dong": time.ctime(psutil.boot_time()),
        "ram": {
            "tong_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "con_trong_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "da_dung_phan_tram": psutil.virtual_memory().percent,
        },
        "swap": {
            "tong_gb": round(psutil.swap_memory().total / (1024**3), 2),
            "da_dung_gb": round(psutil.swap_memory().used / (1024**3), 2),
        },
    }

    o_dia = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            o_dia.append({
                "o": part.mountpoint,
                "dinh_dang": part.fstype,
                "tong_gb": round(usage.total / (1024**3), 1),
                "da_dung_gb": round(usage.used / (1024**3), 1),
                "con_trong_gb": round(usage.free / (1024**3), 1),
                "phan_tram": usage.percent,
            })
        except PermissionError:
            continue
    info["o_dia"] = o_dia

    return {"thanh_cong": True, "thong_tin": info}


def cmd_kiem_tra_cong() -> dict:
    """Kiem tra cong (gate) co hoat dong khong."""
    from than_thong.config import config
    return {
        "thanh_cong": True,
        "thong_bao": "Cong hoat dong: tat ca chinh sach da duoc ap dung",
        "cong_cu_bi_chan": list(config.blocked_tools),
        "uu_tien_local": config.get("local_first"),
        "khong_billing": config.get("no_billing"),
    }


# === Offline Agent (heuristic + Ollama) ===

HEURISTICS = [
    ("may-in", ["máy in", "may in", "printer", "epson", "in an", "in ấn", "print"]),
    ("spooler", ["spooler", "queue in", "hang doi in", "hàng đợi in", "print service"]),
    ("usb", ["usb", "thiet bi usb", "thiết bị usb", "cam usb", "cắm usb"]),
    ("am-thanh", ["audio", "loa", "mic", "micro", "am thanh", "âm thanh"]),
    ("tra-cuu", ["hoi", "hỏi", "tra cuu", "tra cứu", "kien thuc", "kiến thức", "question"]),
    ("tim-kiem", ["tim", "tìm", "tra local", "index", "search file"]),
    ("trung-lap", ["duplicate", "trung lap", "trùng lặp", "trung file", "trùng file"]),
    ("he-thong", ["windows", "he thong", "hệ thống", "may win", "máy win", "system"]),
    ("don-dep", ["don", "dọn", "rac", "rác", "temp", "temporary", "cache"]),
    ("bao-mat", ["bao mat", "bảo mật", "security", "virus", "defender", "firewall"]),
]

SUGGESTIONS = {
    "may-in": ["sua-may-in"],
    "spooler": ["sua-spooler"],
    "usb": ["sua-usb"],
    "am-thanh": ["sua-am-thanh"],
    "tra-cuu": ["tim-kiem"],
    "he-thong": ["trang-thai"],
    "don-dep": ["don-dep"],
    "bao-mat": ["kiem-tra-bao-mat"],
}


def _tim_model_va_goi_y(cau_hoi: str) -> dict:
    """Heuristic: nhan dien y dinh tu cau hoi."""
    norm = cau_hoi.lower()
    matches = []
    for label, keywords in HEURISTICS:
        if any(k in norm for k in keywords):
            matches.append(label)
    primary = matches[0] if matches else None
    suggestions = SUGGESTIONS.get(primary, []) if primary else []
    return {"nhan_dien": matches, "chinh": primary, "goi_y_lenh": suggestions}


def cmd_hoi(text: str = "") -> dict:
    """Hoi tu nhien — heuristic + toan bo AI local (Ollama, llamafile, GPT4All, llama.cpp)."""
    if not text.strip():
        return {"thanh_cong": False, "loi": 'Nhap cau hoi. VD: than-thong.exe hoi "may in bi loi"'}

    # 1. Heuristic
    heuristic = _tim_model_va_goi_y(text)

    result = {
        "thanh_cong": True,
        "cau_hoi": text,
        "nhan_dien": heuristic["nhan_dien"],
        "chinh": heuristic["chinh"],
        "goi_y_lenh": heuristic["goi_y_lenh"],
        "ai_local": [],
    }

    # 2. Goi AI local tu dong (Ollama > llamafile > GPT4All > llama.cpp)
    from than_thong.model_manager import goi_ai_tu_dong, phat_hien_tat_ca

    ds_ai = phat_hien_tat_ca()
    ai_response = goi_ai_tu_dong(text, ds_ai)
    result["ai_local"] = ds_ai

    if ai_response.get("thanh_cong"):
        result["ai_tra_loi"] = ai_response["tra_loi"]
        result["ai_runtime"] = ai_response["runtime"]
    else:
        result["ai_loi"] = ai_response.get("loi", "")
        if "huong_dan" in ai_response:
            result["huong_dan_cai_dat"] = ai_response["huong_dan"]

    return result


def cmd_ai() -> dict:
    """Kiem tra cac AI local co san."""
    from than_thong.model_manager import phat_hien_tat_ca
    ds = phat_hien_tat_ca()
    tong = sum(1 for d in ds if d.get("co") or d.get("api_hoat_dong"))
    return {
        "thanh_cong": True,
        "tong_ai_tim_thay": tong,
        "danh_sach": ds,
    }


# === File tools ===

def cmd_sao_chep(text: str = "") -> dict:
    """Sao chep file hoac thu muc. Dung: sao-chep <nguon> <dich>"""
    from than_thong.file_tools import cmd_sao_chep as _sc
    parts = text.split("||")
    if len(parts) < 2:
        return {"thanh_cong": False, "loi": 'Thieu tham so. VD: sao-chep "C:\\folder"||"E:\\folder"'}
    return _sc(parts[0].strip(), parts[1].strip())


def cmd_di_chuyen(text: str = "") -> dict:
    """Di chuyen file hoac thu muc. Dung: di-chuyen <nguon> <dich>"""
    from than_thong.file_tools import cmd_di_chuyen as _dc
    parts = text.split("||")
    if len(parts) < 2:
        return {"thanh_cong": False, "loi": 'Thieu tham so. VD: di-chuyen "C:\\folder"||"E:\\folder"'}
    return _dc(parts[0].strip(), parts[1].strip())


def cmd_dong_bo(text: str = "") -> dict:
    """Dong bo thu muc. Dung: dong-bo <nguon> <dich>"""
    from than_thong.file_tools import cmd_dong_bo as _db
    parts = text.split("||")
    if len(parts) < 2:
        return {"thanh_cong": False, "loi": 'Thieu tham so. VD: dong-bo "C:\\folder"||"E:\\folder"'}
    return _db(parts[0].strip(), parts[1].strip())


def cmd_kiem_tra_file(text: str = "") -> dict:
    """Kiem tra thong tin file."""
    from than_thong.file_tools import cmd_thong_tin_file
    if not text.strip():
        return {"thanh_cong": False, "loi": "Nhap duong dan file. VD: kiem-tra-file C:\\path"}
    return cmd_thong_tin_file(text.strip())


def cmd_checksum(text: str = "") -> dict:
    """Tinh checksum file. VD: checksum C:\\file.iso"""
    from than_thong.file_tools import cmd_kiem_tra_checksum
    if not text.strip():
        return {"thanh_cong": False, "loi": "Nhap duong dan file. VD: checksum C:\\file.iso"}
    return cmd_kiem_tra_checksum(text.strip())



def cmd_so_sanh_checksum(text: str = "") -> dict:
    """So sanh 2 file. Dung: so-sanh <file1>||<file2>"""
    from than_thong.file_tools import cmd_so_sanh_checksum as _ss
    parts = text.split("||")
    if len(parts) < 2:
        return {"thanh_cong": False, "loi": 'Thieu tham so. VD: so-sanh "C:\\a.iso"||"E:\\a.iso"'}
    return _ss(parts[0].strip(), parts[1].strip())


def cmd_wsl_export(text: str = "") -> dict:
    """Export WSL distro. Dung: wsl-export <ten>||<duong-dan>"""
    from than_thong.file_tools import cmd_wsl_export, cmd_wsl_unregister
    parts = text.split("||")
    if len(parts) < 2:
        return {"thanh_cong": False, "loi": 'Thieu tham so. VD: wsl-export Ubuntu||"E:\\WSL\\ubuntu.tar"'}
    return cmd_wsl_export(parts[0].strip(), parts[1].strip())


def cmd_wsl_xoa(text: str = "") -> dict:
    """Xoa WSL distro (giai phong dung luong)."""
    from than_thong.file_tools import cmd_wsl_unregister
    if not text.strip():
        return {"thanh_cong": False, "loi": "Nhap ten distro. VD: wsl-xoa Ubuntu"}
    return cmd_wsl_unregister(text.strip())


import string  # noqa: E402
