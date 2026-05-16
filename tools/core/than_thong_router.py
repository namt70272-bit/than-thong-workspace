#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
OUT = ROOT / "tools-internal" / "records" / "than-thong-router-last.json"

ROUTES: list[tuple[str, list[str], list[str]]] = [
    ("win-repair-printer", ["máy in", "printer", "print", "epson", "l1250"], ["suggest"]),
    ("win-repair-spooler", ["spooler", "hàng đợi in", "queue in", "print service"], ["suggest"]),
    ("win-events", ["event", "log windows", "printservice", "kernel-pnp", "userpnp"], ["suggest", "24"]),
    ("win-repair-usb", ["usb", "thiết bị usb", "cắm usb", "usb device"], ["suggest"]),
    ("win-repair-audio", ["audio", "âm thanh", "loa", "mic", "micro"], ["suggest"]),
    ("local-search", ["tìm local", "local search", "index file", "tra file local"], []),
    ("docs-miner", ["docs miner", "đào tài liệu", "tóm tài liệu local", "mine docs"], []),
    ("local-qa", ["hỏi tài liệu local", "tra cứu local", "local qa", "knowledge local", "hỏi docs"], []),
    ("win-full", ["windows full", "kiểm tra windows", "dashboard windows", "win full"], []),
    ("win-audit", ["audit windows", "kiểm tra hệ thống windows", "win audit"], []),
    ("win-cleanup", ["dọn rác windows", "cleanup windows", "temp windows", "junk windows"], []),
    ("win-process", ["process windows", "tiến trình windows", "kiểm tra process"], []),
    ("win-data", ["data map", "ổ đĩa", "dữ liệu ổ", "win data"], []),
    ("win-env", ["biến môi trường", "env windows", "win env"], []),
    ("win-svc", ["service windows", "dịch vụ windows", "win svc"], []),
    ("win-startup", ["startup windows", "khởi động cùng windows"], []),
    ("win-disk", ["disk health", "sức khỏe ổ đĩa", "win disk"], []),
    ("win-restore", ["system restore", "điểm khôi phục", "win restore"], []),
    ("win-tighten", ["siết windows", "tighten windows", "win tighten"], []),
    ("duplicate", ["duplicate", "trùng lặp", "file trùng"], []),
    ("canonical", ["canonical", "nhiều nguồn sự thật", "nguồn sự thật"], []),
    ("inventory", ["inventory", "kiểm kê workspace", "kiểm tra workspace"], []),
    ("domains", ["domains", "nhóm domain", "phân vùng domain"], []),
    ("drift", ["drift", "lệch", "so lệch"], []),
    ("waves", ["waves", "wave import", "làn nhập"], []),
    ("dashboard", ["dashboard", "tổng quan nội bộ", "ops dashboard"], []),
    ("scan-G", ["scan g", "quét g", "g ai", "g:\\ai"], []),
    ("daily", ["daily", "bảo trì ngày", "duy trì hàng ngày"], []),
]

BLOCKED_HINTS = [
    "openai", "claude api", "gemini api", "anthropic api", "billing", "topup", "top-up",
    "quota", "quata", "credit", "credits", "token paid", "provider paid", "api key trả phí",
    "firecrawl api", "pinecone cloud", "qdrant cloud", "external paid"
]

EXTERNAL_HINTS = [
    "web", "internet", "search online", "google", "browse", "fetch url", "api ngoài"
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def route_text(text: str) -> dict:
    norm = normalize(text)

    for hint in BLOCKED_HINTS:
        if hint in norm:
            return {
                "status": "blocked",
                "reason": "billing-or-quota-risk",
                "message": "Lệnh có dấu hiệu chạm billing/quota/provider trả phí; thần thông chặn ở cửa đầu tiên.",
            }

    for hint in EXTERNAL_HINTS:
        if hint in norm:
            return {
                "status": "unsupported",
                "reason": "needs-external-review",
                "message": "Lệnh có dấu hiệu cần external/internet. Theo rule hiện tại, phải giữ local-first và tránh billing/quota.",
            }

    for command, keywords, args in ROUTES:
        if any(k in norm for k in keywords):
            return {
                "status": "ok",
                "command": command,
                "args": args,
                "message": f"Route tới `{command}`",
            }

    return {
        "status": "unsupported",
        "reason": "no-local-route",
        "message": "Thần thông chưa có route local an toàn cho yêu cầu này.",
    }


def main() -> int:
    raw = " ".join(sys.argv[1:]).strip()
    result = route_text(raw)
    payload = {"input": raw, **result}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
