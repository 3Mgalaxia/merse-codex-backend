from fastapi import APIRouter, HTTPException

from app.schemas.edit_request import EditRequest
from app.schemas.edit_response import EditResponse
from app.services.openai_client import OpenAIClientSingleton
from app.services.model_selector import CodexTask, escolher_modelo
from app.utils.cost import estimar_custo_usd
from app.utils.prompts import prompt_edit_site
from app.utils.validate import safe_len

router = APIRouter()


@router.post("/edit-site", response_model=EditResponse)
async def edit_site(payload: EditRequest) -> EditResponse:
    client = OpenAIClientSingleton.get_client()

    html_len = safe_len(payload.html)
    comando_len = safe_len(payload.comando)

    modelo = escolher_modelo(
        task=CodexTask.EDIT,
        html_len=html_len,
        comando_len=comando_len,
    )

    prompt = prompt_edit_site(payload.html, payload.comando)

    try:
        completion = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Você é o Merse Codex, editor de HTML da Merse."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar modelo: {e}")

    message = completion.choices[0].message.content or ""

    usage = getattr(completion, "usage", None)
    tokens_prompt = getattr(usage, "prompt_tokens", None) if usage else None
    tokens_resposta = getattr(usage, "completion_tokens", None) if usage else None
    tokens_total = getattr(usage, "total_tokens", None) if usage else None

    custo_estimado = estimar_custo_usd(tokens_total, modelo) if tokens_total else None

    return EditResponse(
        html_atualizado=message.strip(),
        tokens_usados_prompt=tokens_prompt,
        tokens_usados_resposta=tokens_resposta,
        modelo=modelo,
        custo_estimado_usd=custo_estimado,
    )