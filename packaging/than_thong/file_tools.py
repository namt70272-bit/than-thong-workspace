"""Cong cu quan ly file — copy nhanh, di chuyen, dong bo, xac thuc."""
import os, sys, shutil, subprocess, json, hashlib, time, threading
from pathlib import Path
from than_thong.logger import log


class ProgressTracker:
    """Theo doi tien trinh copy file."""
    def __init__(self, total_bytes=0, label=""):
        self.total = total_bytes
        self.done = 0
        self.label = label
        self._start = time.time()
        self._lock = threading.Lock()

    def add(self, n):
        with self._lock:
            self.done += n

    def report(self):
        with self._lock:
            pct = (self.done / self.total * 100) if self.total else 0
            elapsed = time.time() - self._start
            speed = self.done / (1024*1024) / elapsed if elapsed > 0 else 0
            return {
                "da_copy_mb": round(self.done / (1024*1024), 1),
                "tong_mb": round(self.total / (1024*1024), 1),
                "phan_tram": round(pct, 1),
                "toc_do_mb_s": round(speed, 1),
                "thoi_gian_giay": round(elapsed, 1),
                "nhan": self.label,
            }


def _robocopy(src: str, dst: str, mt: int = 8) -> dict:
    """Copy folder bang robocopy (Windows native, multi-thread)."""
    if not os.path.isdir(src):
        return {"thanh_cong": False, "loi": "Thu muc nguon khong ton tai: " + src}
    os.makedirs(dst, exist_ok=True)

    cmd = [
        "robocopy", src, dst,
        "/E",                       # Copy subdirs
        "/COPY:DAT",                # Copy data+attributes+timestamps
        f"/MT:{mt}",                # Multi-thread
        "/R:2", "/W:1",             # Retry 2 lan, wait 1s
        "/NFL", "/NDL",             # Khong log tung file
        "/NP",                      # Khong log %
        "/NJH", "/NJS",             # Bo header, summary
    ]
    log.info("Robocopy: %s -> %s (threads=%d)", src, dst, mt)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        exit_code = r.returncode
        # robocopy: 0=no change, 1=ok, 2+=extra files, 3+=some errors
        ok = exit_code < 8
        return {
            "thanh_cong": ok,
            "ma_thoat": exit_code,
            "chitiet": r.stdout[-1000:] if r.stdout else "",
        }
    except subprocess.TimeoutExpired:
        return {"thanh_cong": False, "loi": "Qua thoi gian (1 gio)"}
    except Exception as e:
        return {"thanh_cong": False, "loi": str(e)}


def cmd_sao_chep(src: str, dst: str, mt: int = 8) -> dict:
    """Sao chep file hoac thu muc, tu dong chon phuong thuc nhanh nhat."""
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    if not os.path.exists(src):
        return {"thanh_cong": False, "loi": "Khong tim thay: " + src}
    if src == dst:
        return {"thanh_cong": False, "loi": "Nguon va dich giong nhau"}

    # Tinh kich thuoc
    if os.path.isfile(src):
        total = os.path.getsize(src)
        is_folder = False
    else:
        total = sum(f.stat().st_size for f in Path(src).rglob('*') if f.is_file())
        is_folder = True

    pt = ProgressTracker(total, f"Copy {os.path.basename(src)}")
    log.info("Bat dau copy: %s (%d MB)", src, total/(1024*1024))

    t0 = time.time()
    if is_folder:
        # Dung robocopy cho thu muc (nhanh hon nhieu)
        result = _robocopy(src, dst, mt)
        elapsed = time.time() - t0
        result["thoi_gian_giay"] = round(elapsed, 1)
        result["toc_do_mb_s"] = round(total / (1024*1024) / elapsed, 1) if elapsed > 0 else 0
        result["nguon"] = src
        result["dich"] = dst
        result["kich_thuoc_mb"] = round(total / (1024*1024), 1)
        if result.get("thanh_cong"):
            result["thong_bao"] = "Sao chep hoan tat: %s -> %s" % (src, dst)
        return result
    else:
        # File don: dung shutil copy2
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            elapsed = time.time() - t0
            return {
                "thanh_cong": True,
                "nguon": src,
                "dich": dst,
                "kich_thuoc_mb": round(total / (1024*1024), 1),
                "thoi_gian_giay": round(elapsed, 1),
                "toc_do_mb_s": round(total / (1024*1024) / elapsed, 1) if elapsed > 0 else 0,
                "thong_bao": "Sao chep hoan tat: %s (%d MB)" % (os.path.basename(src), total/(1024*1024)),
            }
        except Exception as e:
            return {"thanh_cong": False, "loi": str(e)}


def cmd_di_chuyen(src: str, dst: str, mt: int = 8) -> dict:
    """Di chuyen file hoac thu muc. Copy xong moi xoa goc."""
    if not os.path.exists(src):
        return {"thanh_cong": False, "loi": "Khong tim thay: " + src}

    # Thu rename truoc (nhanh nhat, cung partition)
    try:
        os.rename(src, dst)
        log.info("Di chuyen (rename): %s -> %s", src, dst)
        return {
            "thanh_cong": True,
            "nguon": src,
            "dich": dst,
            "phuong_thuc": "rename (cung partition)",
            "thong_bao": "Di chuyen hoan tat: %s" % os.path.basename(src),
        }
    except OSError:
        pass  # Khac partition, can copy + xoa

    # Copy truoc
    result = cmd_sao_chep(src, dst, mt)
    if result.get("thanh_cong"):
        # Xoa goc
        try:
            if os.path.isfile(src):
                os.remove(src)
            else:
                shutil.rmtree(src)
            result["da_xoa_goc"] = True
            result["phuong_thuc"] = "copy+delete (khac partition)"
            result["thong_bao"] = "Di chuyen hoan tat: %s" % os.path.basename(src)
        except Exception as e:
            result["da_xoa_goc"] = False
            result["canh_bao"] = "Copy xong nhung khong xoa duoc goc: " + str(e)
    return result


def cmd_dong_bo(src: str, dst: str, mt: int = 8) -> dict:
    """Dong bo thu muc nguon -> dich (mirror)."""
    if not os.path.isdir(src):
        return {"thanh_cong": False, "loi": "Thu muc nguon khong ton tai: " + src}

    os.makedirs(dst, exist_ok=True)
    cmd = [
        "robocopy", src, dst,
        "/MIR",                     # Mirror (copy + xoa file thua o dich)
        "/COPY:DAT",
        f"/MT:{mt}",
        "/R:2", "/W:1",
        "/NFL", "/NDL", "/NP", "/NJH", "/NJS",
    ]
    log.info("Dong bo: %s -> %s", src, dst)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        ok = r.returncode < 8
        return {
            "thanh_cong": ok,
            "ma_thoat": r.returncode,
            "nguon": src,
            "dich": dst,
            "chitiet": r.stdout[-1000:] if r.stdout else "",
        }
    except Exception as e:
        return {"thanh_cong": False, "loi": str(e)}


def cmd_kiem_tra_checksum(file_path: str, algorithm: str = "sha256") -> dict:
    """Tinh checksum file de xac thuc tinh toan ven."""
    if not os.path.isfile(file_path):
        return {"thanh_cong": False, "loi": "File khong ton tai: " + file_path}

    size = os.path.getsize(file_path)
    log.info("Tinh %s: %s (%d MB)...", algorithm, file_path, size/(1024*1024))

    h = hashlib.new(algorithm)
    t0 = time.time()
    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(64 * 1024)  # 64KB buffer
                if not chunk:
                    break
                h.update(chunk)
        elapsed = time.time() - t0
        checksum = h.hexdigest()
        return {
            "thanh_cong": True,
            "file": file_path,
            "thuat_toan": algorithm,
            "checksum": checksum,
            "kich_thuoc_mb": round(size / (1024*1024), 1),
            "thoi_gian_giay": round(elapsed, 1),
        }
    except Exception as e:
        return {"thanh_cong": False, "loi": str(e)}


def cmd_so_sanh_checksum(file1: str, file2: str) -> dict:
    """So sanh 2 file bang checksum."""
    r1 = cmd_kiem_tra_checksum(file1)
    if not r1.get("thanh_cong"):
        return r1
    r2 = cmd_kiem_tra_checksum(file2)
    if not r2.get("thanh_cong"):
        return r2

    giong = r1["checksum"] == r2["checksum"]
    return {
        "thanh_cong": True,
        "file1": file1,
        "file2": file2,
        "checksum1": r1["checksum"],
        "checksum2": r2["checksum"],
        "giong_nhau": giong,
        "thong_bao": "Giong nhau" if giong else "KHAC nhau",
    }


def cmd_thong_tin_file(path: str) -> dict:
    """Xem thong tin chi tiet ve file hoac thu muc."""
    if not os.path.exists(path):
        return {"thanh_cong": False, "loi": "Khong tim thay: " + path}

    path = os.path.abspath(path)
    stat = os.stat(path)

    info = {
        "duong_dan": path,
        "ten": os.path.basename(path),
        "loai": "file" if os.path.isfile(path) else "thu_muc" if os.path.isdir(path) else "khac",
        "kich_thuoc": stat.st_size,
        "kich_thuoc_mb": round(stat.st_size / (1024*1024), 1),
        "tao_luc": time.ctime(stat.st_ctime),
        "sua_luc": time.ctime(stat.st_mtime),
        "truy_cap_luc": time.ctime(stat.st_atime),
    }

    if os.path.isdir(path):
        files = list(Path(path).rglob('*'))
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        info["so_file"] = len([f for f in files if f.is_file()])
        info["so_thu_muc"] = len([f for f in files if f.is_dir()])
        info["tong_dung_luong_mb"] = round(total_size / (1024*1024), 1)
        # File lon nhat
        if files:
            biggest = max((f for f in files if f.is_file()), key=lambda f: f.stat().st_size, default=None)
            if biggest:
                info["file_lon_nhat"] = str(biggest)
                info["file_lon_nhat_mb"] = round(biggest.stat().st_size / (1024*1024), 1)

    return {"thanh_cong": True, "thong_tin": info}


# === WSL tools ===

def cmd_wsl_export(ten_distro: str, duong_dan: str) -> dict:
    """Export WSL distro ra file tar."""
    if not duong_dan.endswith(".tar"):
        duong_dan += ".tar"
    log.info("Export WSL: %s -> %s", ten_distro, duong_dan)
    try:
        r = subprocess.run(
            ["wsl", "--export", ten_distro, duong_dan],
            capture_output=True, text=True, timeout=600
        )
        if r.returncode == 0:
            size = os.path.getsize(duong_dan) if os.path.exists(duong_dan) else 0
            return {
                "thanh_cong": True,
                "distro": ten_distro,
                "file": duong_dan,
                "dung_luong_mb": round(size / (1024*1024), 1),
            }
        return {"thanh_cong": False, "loi": r.stderr or r.stdout}
    except Exception as e:
        return {"thanh_cong": False, "loi": str(e)}


def cmd_wsl_unregister(ten_distro: str) -> dict:
    """Xoa WSL distro (giai phong dung luong)."""
    log.info("Xoa WSL distro: %s", ten_distro)
    try:
        r = subprocess.run(
            ["wsl", "--unregister", ten_distro],
            capture_output=True, text=True, timeout=30
        )
        return {"thanh_cong": r.returncode == 0, "distro": ten_distro, "chitiet": r.stdout or r.stderr}
    except Exception as e:
        return {"thanh_cong": False, "loi": str(e)}
