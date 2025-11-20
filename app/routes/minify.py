from fastapi import APIRouter, HTTPException

from app.schemas.edit_request import EditRequest
from app.schemas.edit_response import EditResponse
from app.services.codex_engine import CodexEngine
from app.services.model_selector import CodexTask, escolher_modelo
from app.utils.cost import estimar_custo_usd
from app.utils.prompts import prompt_minify
from app.utils.validate import safe_len

router = APIRouter()


@router.post("/minify", response_model=EditResponse)
async def minify_html(payload: EditRequest) -> EditResponse:
    html_len = safe_len(payload.html)
    comando_len = safe_len(payload.comando)

    modelo = escolher_modelo(
        task=CodexTask.MINIFY,
        html_len=html_len,
        comando_len=comando_len,
    )

    prompt = prompt_minify(payload.html, payload.comando)

    try:
        resultado = CodexEngine.run(
            model=modelo,
            system_prompt="Você é o Merse Codex focado em otimizar e minificar HTML/CSS/JS.",
            user_prompt=prompt,
            temperature=0.1,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao minificar HTML: {exc}")

    custo = estimar_custo_usd(resultado.total_tokens, modelo) if resultado.total_tokens else None

    return EditResponse(
        html_atualizado=resultado.content,
        tokens_usados_prompt=resultado.prompt_tokens,
        tokens_usados_resposta=resultado.completion_tokens,
        modelo=modelo,
        custo_estimado_usd=custo,
    )
