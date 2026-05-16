#!/usr/bin/env python3
"""Than-thong GPU — chay local LLM tren RTX 3060 (CUDA)

Dung:
  python than_thong_gpu.py "cau hoi cua ban"
"""
import os, sys, json, time, urllib.request, urllib.error

# === Cau hinh ===
OLLAMA_HOST = "http://localhost:11434"
LOCAL_MODEL = "qwen2.5-coder:7b"  # Model co san trong Ollama

def check_gpu() -> dict:
    """Kiem tra GPU co san khong."""
    info = {
        "gpu": False,
        "cuda": False,
        "ollama": False,
        "model": None,
    }
    # Check CUDA via PyTorch
    try:
        import torch
        info["cuda"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            info["gpu"] = True
            info["gpu_name"] = torch.cuda.get_device_name(0)
            info["vram_gb"] = round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)
    except ImportError:
        pass

    # Check Ollama
    try:
        r = urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=2)
        if r.status == 200:
            data = json.loads(r.read())
            models = [m["name"] for m in data.get("models", [])]
            info["ollama"] = True
            info["models"] = models
            if models:
                info["model"] = models[0]
    except Exception:
        pass

    return info


def query_ollama(prompt: str, model: str = None) -> dict:
    """Goi Ollama local (chay tren GPU)."""
    if not model:
        info = check_gpu()
        model = info.get("model", LOCAL_MODEL)
        if not info["ollama"]:
            return {"thanh_cong": False, "loi": "Ollama khong chay. Khoi dong: ollama serve"}

    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_gpu": -1,  # Dung toan bo GPU
            "num_thread": 8,
        }
    }).encode()

    t0 = time.time()
    try:
        r = urllib.request.urlopen(
            f"{OLLAMA_HOST}/api/generate",
            data=body,
            timeout=60
        )
        data = json.loads(r.read())
        elapsed = time.time() - t0

        return {
            "thanh_cong": True,
            "tra_loi": data.get("response", ""),
            "model": model,
            "thoi_gian_giay": round(elapsed, 1),
            "tokens_giay": round(data.get("eval_count", 0) / elapsed, 1) if elapsed > 0 else 0,
        }
    except urllib.error.HTTPError as e:
        return {"thanh_cong": False, "loi": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"thanh_cong": False, "loi": str(e)}


def main():
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not text:
        text = sys.stdin.read().strip() if not sys.stdin.isatty() else ""

    if not text or text in ("--help", "-h", "status", "info"):
        info = check_gpu()
        print(json.dumps({
            "thanh_cong": True,
            "gpu_info": info,
            "huong_dan": "Dung: python than_thong_gpu.py \"cau hoi cua ban\"",
        }, ensure_ascii=False, indent=2))
        return

    result = query_ollama(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
