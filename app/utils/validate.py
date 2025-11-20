def safe_len(text: str | None) -> int:
    if not text:
        return 0
    return len(text)