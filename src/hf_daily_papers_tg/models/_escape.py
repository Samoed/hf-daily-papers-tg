def escape(text: str | int | None) -> str:
    """Escape HTML special characters."""
    if text is None:
        return ""
    text = str(text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
