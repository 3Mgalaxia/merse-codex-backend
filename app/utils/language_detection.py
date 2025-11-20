import re
from typing import Final

LANGUAGE_ALIASES: Final[dict[str, str]] = {
    "html": "html",
    "htm": "html",
    "react": "react",
    "jsx": "react",
    "tsx": "react",
    "tailwind": "tailwind",
    "css": "css",
    "scss": "css",
    "sass": "css",
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "py": "python",
    "python": "python",
    "sql": "sql",
    "java": "java",
}

LANGUAGE_GUIDELINES: Final[dict[str, str]] = {
    "html": "Retorne HTML/CSS válido. Preserve a hierarquia de tags e não deixe elementos sem fechamento.",
    "tailwind": "Retorne HTML usando utilitários Tailwind. Evite estilos inline e garanta classes coerentes.",
    "react": "Retorne um componente React funcional em JSX. Use className, mantenha hooks e não inclua importações supérfluas.",
    "css": "Retorne apenas CSS válido. Não adicione comentários e mantenha seletores consistentes.",
    "javascript": "Retorne JavaScript/TypeScript limpo. Não crie variáveis globais desnecessárias.",
    "typescript": "Retorne TypeScript moderno, tipando parâmetros e retornos quando possível.",
    "python": "Retorne Python idiomático. Preserve indentação de 4 espaços e evite alterar a API pública.",
    "sql": "Retorne SQL compatível com ANSI. Formate cláusulas em linhas separadas.",
    "java": "Retorne Java válido, mantendo nomes de classes/métodos existentes.",
    "auto": "Preserve a linguagem original do trecho. Caso não tenha certeza, mantenha a estrutura atual intacta.",
}


def _normalize_language(value: str | None) -> str:
    if not value:
        return "auto"
    normalized = value.strip().lower()
    return LANGUAGE_ALIASES.get(normalized, normalized or "auto")


def detect_language(code: str, preferred: str | None) -> str:
    normalized = _normalize_language(preferred)
    if normalized != "auto":
        return normalized

    snippet = (code or "").strip()
    lowered = snippet.lower()

    if "<react-component" in lowered or "className=" in snippet or "useState(" in snippet:
        return "react"
    if re.search(r"</?(?:html|body|section|div|header|footer|main)\b", lowered):
        if re.search(r'class(?:Name)?="[^"]*(?:bg-|text-|flex|grid)', snippet):
            return "tailwind"
        return "html"
    if re.search(r'class="[^"]*(?:bg-|text-|flex|grid)', snippet):
        return "tailwind"
    if re.search(r"\b(def|async def)\s+\w+\(", lowered):
        return "python"
    if re.search(r"\bfunction\b|\bconst\s+\w+\s*=\s*\(", snippet):
        return "javascript"
    if re.search(r"\binterface\b|\btype\s+\w+\s*=", lowered):
        return "typescript"
    if "SELECT " in snippet.upper() and (" FROM " in snippet.upper() or " WHERE " in snippet.upper()):
        return "sql"
    if re.search(r"\bpublic\s+class\b", snippet):
        return "java"

    return "auto"


def language_guideline(language: str) -> str:
    return LANGUAGE_GUIDELINES.get(language, LANGUAGE_GUIDELINES["auto"])
