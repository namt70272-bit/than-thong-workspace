"""
Prompt utilities (adapted from autoTriage + Agent365-devTools)
- Load prompts from YAML files
- Sanitize LLM input/output
- Sanitize exception messages (redact credentials)
"""
import re
import logging
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Giới hạn độ dài input mặc định (tránh token overflow)
MAX_TITLE_LENGTH: int = 200
MAX_BODY_LENGTH: int = 2000


def load_prompts(path: str) -> Dict[str, str]:
    """Load prompts from a YAML file.
    
    Expected format:
        prompt_name: |
          system prompt text here...
    
    Returns dict of {prompt_name: prompt_text}
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if not isinstance(data, dict):
        raise ValueError(f"Invalid prompts format in {path}")
    
    return data


def render_prompt(template: str, variables: Dict[str, Any]) -> str:
    """Render a prompt template with variables.
    
    Uses {variable_name} syntax (not f-strings) for safety.
    """
    for key, value in variables.items():
        template = template.replace(f'{{{key}}}', str(value))
    return template


def sanitize_user_content(text: str, max_length: int = MAX_BODY_LENGTH) -> str:
    """Sanitize user input before sending to LLM.

    - Truncates to max_length (log khi cắt)
    - Strips C0 control characters (giữ \n, \t)
    - Escape XML special chars để chống prompt injection qua XML tags
    """
    if not text:
        return ""
    if len(text) > max_length:
        logger.info("Truncated input from %d to %d characters", len(text), max_length)
        text = text[:max_length]
    # Strip C0 control chars trừ tab (0x09) và newline (0x0a)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    # Escape XML — & phải đi trước để tránh double-encode
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return text


def sanitize_exception(e: Exception) -> str:
    """Trả về string của exception với credentials đã được redact.

    Một số LLM client (openai, requests) nhúng API key / Bearer token
    vào exception message. Hàm này redact trước khi log.
    """
    text = str(e)
    # Pass 1: Bearer token
    text = re.sub(r'(?i)Bearer\s+[A-Za-z0-9\-._~+/]+=*', 'Bearer [REDACTED]', text)
    # Pass 2: key=value / key: value credential pairs
    text = re.sub(
        r'(?i)(authorization|api.?key|token|secret|password|client.?secret)'
        r'["\']?\s*[:=]\s*["\']?[^\s"\']*',
        r'\1=[REDACTED]',
        text,
    )
    # Pass 3: OpenAI-style API key (sk-...)
    text = re.sub(r'sk-[A-Za-z0-9\-]{20,}', '[REDACTED]', text)
    return text


def sanitize_llm_output(text: str) -> str:
    """Sanitize LLM output.
    
    - Strips markdown code fences from JSON blocks
    - Strips BOM characters
    """
    if not text:
        return ""
    # Remove BOM
    text = text.lstrip('\ufeff')
    # Strip markdown JSON fences
    text = text.strip()
    if text.startswith('```'):
        text = text[text.index('\n') + 1:] if '\n' in text else text[3:]
    if text.endswith('```'):
        text = text[:-3].strip()
    return text.strip()
