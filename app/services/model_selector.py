from enum import Enum


class CodexTask(str, Enum):
    EDIT = "edit"
    EXECUTE = "execute"
    ANALYSE = "analyse"
    REFACTOR = "refactor"
    BEAUTIFY = "beautify"
    SEO = "seo"
    CONVERT_REACT = "convert-react"
    CONVERT_TAILWIND = "convert-tailwind"
    COMPONENTIZE = "componentize"
    REPAIR = "repair"
    MINIFY = "minify"


def escolher_modelo(
    task: CodexTask,
    html_len: int,
    comando_len: int,
) -> str:
    """
    Lógica de seleção automática de modelo.
    Você pode tunar isso depois, mas já nasce em nível pro.
    """

    # thresholds simples (caracteres)
    pequeno = 2_000
    medio = 8_000

    # 1) Tarefas pesadas de código → favorece gpt-4.1
    if task in {CodexTask.CONVERT_REACT, CodexTask.REFACTOR, CodexTask.REPAIR}:
        if html_len > medio or comando_len > 500:
            return "gpt-4.1-mini"  # você pode trocar para gpt-4.1
        return "gpt-4o"

    # 2) Análises & SEO → gpt-4o
    if task in {CodexTask.ANALYSE, CodexTask.SEO, CodexTask.COMPONENTIZE}:
        if html_len > medio:
            return "gpt-4o"
        return "gpt-4o-mini"

    # 3) Execução universal tem heurística própria
    if task == CodexTask.EXECUTE:
        if html_len > medio or comando_len > 600:
            return "gpt-4.1-mini"
        if html_len < pequeno and comando_len < 250:
            return "gpt-4o-mini"
        return "gpt-4o"

    # 4) Edição simples / Beautify / Minify → gpt-4o-mini por padrão
    if task in {CodexTask.EDIT, CodexTask.BEAUTIFY, CodexTask.MINIFY}:
        if html_len < pequeno and comando_len < 300:
            return "gpt-4o-mini"
        return "gpt-4o"

    # fallback
    return "gpt-4o-mini"
