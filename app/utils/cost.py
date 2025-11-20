from typing import Optional


def estimar_custo_usd(
    total_tokens: Optional[int],
    modelo: str,
) -> Optional[float]:
    """
    Estimativa aproximada de custo por tokens.
    Você pode ajustar depois com os valores oficiais da OpenAI.
    Aqui é só para mostrar custo estimado no painel da Merse.
    """
    if total_tokens is None:
        return None

    # valores "chute" só para visual
    preco_por_mil = 0.0006

    if "gpt-4.1" in modelo:
        preco_por_mil = 0.002
    elif "gpt-4o" in modelo:
        preco_por_mil = 0.001
    elif "gpt-4o-mini" in modelo:
        preco_por_mil = 0.0006

    return (total_tokens / 1000.0) * preco_por_mil