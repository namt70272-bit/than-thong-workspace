"""Quan ly model AI local — phat hien va goi Ollama, llamafile, GPT4All, llama.cpp."""
import json, os, subprocess, sys, shutil, urllib.request, urllib.error
from pathlib import Path
from than_thong.logger import log


# === Constants ===

LLAMAFILE_DOWNLOAD = "https://github.com/Mozilla-Ocho/llamafile/releases/latest"
GPT4ALL_API_PORT = 4891  # default GPT4All API port
LLAMA_CPP_API_PORT = 8080  # default llama-server port

COMMON_PATHS = {
    "ollama": [
        r"C:\Users\ACER\AppData\Local\Programs\Ollama\ollama.exe",
        r"C:\Program Files\Ollama\ollama.exe",
    ],
    "llamafile": [
        r"C:\Users\ACER\AppData\Local\llamafile\llamafile.exe",
        r"C:\Users\ACER\Downloads\llamafile.exe",
    ],
    "gpt4all": [
        r"C:\Program Files\GPT4All\gpt4all.exe",
        r"C:\Users\ACER\AppData\Local\Programs\GPT4All\gpt4all.exe",
    ],
    "llama_cpp": [
        r"C:\Users\ACER\AppData\Local\llama.cpp\llama-server.exe",
        r"C:\Users\ACER\AppData\Local\llama.cpp\llama-cli.exe",
    ],
}


def _check_path(name: str) -> str | None:
    """Kiem tra PATH hoac common paths."""
    # Check PATH
    which = shutil.which(name)
    if which:
        return which
    which = shutil.which(name + ".exe")
    if which:
        return which
    # Check common locations
    for p in COMMON_PATHS.get(name, []):
        if os.path.isfile(p):
            return p
    return None


def _check_url(url: str, timeout: float = 0.5) -> bool:
    """Kiem tra URL co tra ve 200 khong."""
    try:
        r = urllib.request.urlopen(url, timeout=timeout)
        return r.status == 200
    except Exception:
        return False


def phat_hien_ollama() -> dict:
    """Phat hien Ollama runtime."""
    exe = _check_path("ollama")
    if not exe:
        return {"co": False}
    models = []
    try:
        r = subprocess.run([exe, "list"], capture_output=True, text=True, timeout=10)
        for line in r.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if parts:
                models.append(parts[0])
    except Exception:
        pass
    # Check API
    api_ok = _check_url("http://localhost:11434/api/tags")
    return {
        "co": True,
        "duong_dan": exe,
        "models": models,
        "api_hoat_dong": api_ok,
    }


def phat_hien_llamafile() -> dict:
    """Phat hien llamafile runtime."""
    exe = _check_path("llamafile")
    if not exe:
        return {"co": False}
    # llamafile runs its own API at port 8080 by default
    api_ok = _check_url("http://localhost:8080/v1/models")
    return {
        "co": True,
        "duong_dan": exe,
        "api_hoat_dong": api_ok,
    }


def phat_hien_gpt4all() -> dict:
    """Phat hien GPT4All runtime."""
    exe = _check_path("gpt4all")
    if not exe:
        # Check API directly
        api_ok = _check_url(f"http://localhost:{GPT4ALL_API_PORT}/api/v1/chat/completions")
        if api_ok:
            return {"co": True, "duong_dan": None, "api_hoat_dong": True}
        return {"co": False}
    api_ok = _check_url(f"http://localhost:{GPT4ALL_API_PORT}/api/v1/chat/completions")
    return {
        "co": True,
        "duong_dan": exe,
        "api_hoat_dong": api_ok,
    }


def phat_hien_llamacpp() -> dict:
    """Phat hien llama.cpp runtime (llama-server)."""
    exe = _check_path("llama-server")
    if not exe:
        api_ok = _check_url(f"http://localhost:{LLAMA_CPP_API_PORT}/v1/models")
        if api_ok:
            return {"co": True, "duong_dan": None, "api_hoat_dong": True}
        return {"co": False}
    api_ok = _check_url(f"http://localhost:{LLAMA_CPP_API_PORT}/v1/models")
    return {
        "co": True,
        "duong_dan": exe,
        "api_hoat_dong": api_ok,
    }


def phat_hien_tat_ca() -> list[dict]:
    """Phat hien tat ca AI runtime."""
    results = []
    for name, fn in [
        ("Ollama", phat_hien_ollama),
        ("llamafile", phat_hien_llamafile),
        ("GPT4All", phat_hien_gpt4all),
        ("llama.cpp", phat_hien_llamacpp),
    ]:
        try:
            info = fn()
            info["ten"] = name
            results.append(info)
        except Exception as e:
            results.append({"ten": name, "co": False, "loi": str(e)})
    return results


def goi_ollama(cau_hoi: str, model: str = None) -> str | None:
    """Goi Ollama API."""
    phat_hien = phat_hien_ollama()
    if not phat_hien.get("api_hoat_dong"):
        return None
    if not model and phat_hien.get("models"):
        model = phat_hien["models"][0]
    if not model:
        model = "llama3.2:1b"

    body = json.dumps({
        "model": model,
        "prompt": f"Nguoi dung hoi: {cau_hoi}\nTra loi bang tieng Viet, ngan gon, de hieu.",
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        r = urllib.request.urlopen(req, timeout=30)
        data = json.loads(r.read())
        return data.get("response", "")
    except Exception as e:
        log.warning("Ollama API loi: %s", e)
        return None


def goi_llamafile(cau_hoi: str) -> str | None:
    """Goi llamafile API (OpenAI-compatible)."""
    body = json.dumps({
        "model": "default",
        "messages": [{"role": "user", "content": cau_hoi}],
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        "http://localhost:8080/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        r = urllib.request.urlopen(req, timeout=30)
        data = json.loads(r.read())
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        log.warning("llamafile API loi: %s", e)
        return None


def goi_gpt4all(cau_hoi: str) -> str | None:
    """Goi GPT4All API."""
    body = json.dumps({
        "model": "default",
        "messages": [{"role": "user", "content": cau_hoi}],
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        f"http://localhost:{GPT4ALL_API_PORT}/api/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        r = urllib.request.urlopen(req, timeout=30)
        data = json.loads(r.read())
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        log.warning("GPT4All API loi: %s", e)
        return None


def goi_llamacpp(cau_hoi: str) -> str | None:
    """Goi llama.cpp API (OpenAI-compatible)."""
    body = json.dumps({
        "model": "default",
        "messages": [{"role": "user", "content": cau_hoi}],
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        f"http://localhost:{LLAMA_CPP_API_PORT}/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        r = urllib.request.urlopen(req, timeout=30)
        data = json.loads(r.read())
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        log.warning("llama.cpp API loi: %s", e)
        return None


def goi_ai_tu_dong(cau_hoi: str, ket_qua_phat_hien: list = None) -> dict:
    """Tu dong tim AI runtime dang chay va goi.
    Nhan ket_qua_phat_hien tu phat_hien_tat_ca() de tranh goi lai."""
    if ket_qua_phat_hien is None:
        ket_qua_phat_hien = phat_hien_tat_ca()

    # Thu tu uu tien: Ollama > llamafile > GPT4All > llama.cpp
    for info in ket_qua_phat_hien:
        ten = info.get("ten", "")
        fn = {
            "Ollama": goi_ollama,
            "llamafile": goi_llamafile,
            "GPT4All": goi_gpt4all,
            "llama.cpp": goi_llamacpp,
        }.get(ten)
        if not fn:
            continue
        if info.get("api_hoat_dong") or info.get("co"):
            tra_loi = fn(cau_hoi)
            if tra_loi:
                return {
                    "thanh_cong": True,
                    "runtime": ten,
                    "tra_loi": tra_loi,
                    "chi_tiet": info,
                }
            return {
                "thanh_cong": False,
                "runtime": ten,
                "loi": "Khong nhan duoc phan hoi tu AI",
                "chi_tiet": info,
            }

    return {
        "thanh_cong": False,
        "runtime": None,
        "loi": "Khong tim thay AI local nao. Cai Ollama, llamafile, GPT4All hoac llama.cpp.",
        "huong_dan": {
            "ollama": "https://ollama.com/download",
            "llamafile": "https://github.com/Mozilla-Ocho/llamafile",
            "gpt4all": "https://gpt4all.io",
            "llama.cpp": "https://github.com/ggerganov/llama.cpp",
        },
    }
