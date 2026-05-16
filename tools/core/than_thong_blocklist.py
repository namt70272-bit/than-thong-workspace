#!/usr/bin/env python3
from __future__ import annotations

BLOCKED_HINTS = [
    "openai", "anthropic", "claude api", "gemini api", "openrouter", "perplexity api",
    "billing", "topup", "top-up", "quota", "quata", "credit", "credits",
    "api key trả phí", "provider paid", "token trả phí", "gọi model trả phí",
    "firecrawl api", "pinecone cloud", "qdrant cloud", "weaviate cloud", "milvus cloud",
    "azure openai", "bedrock", "vertex ai", "cohere api", "mistral api"
]

EXTERNAL_HINTS = [
    "web", "internet", "online", "google", "search online", "browse", "fetch url", "api ngoài"
]


def inspect(text: str) -> dict:
    lower = text.lower()
    for hint in BLOCKED_HINTS:
        if hint in lower:
            return {
                "blocked": True,
                "reason": "billing-or-quota-risk",
                "matched": hint,
                "message": "Request có dấu hiệu dùng billing/quota/provider trả phí; thần thông chặn ngay."
            }
    for hint in EXTERNAL_HINTS:
        if hint in lower:
            return {
                "blocked": True,
                "reason": "external-risk",
                "matched": hint,
                "message": "Request có dấu hiệu cần external/internet; thần thông giữ local-first và chặn tại cửa đầu tiên."
            }
    return {
        "blocked": False,
        "reason": None,
        "matched": None,
        "message": "ok"
    }
