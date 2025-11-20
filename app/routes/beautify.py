from fastapi import APIRouter, HTTPException

from app.schemas.edit_request import EditRequest
from app.schemas.edit_response import EditResponse
from app.services.openai_client import OpenAIClientSingleton
from app.services.model_selector import CodexTask, escolher_modelo
from app.utils.cost import estimar_custo_usd
from app.utils.validate import safe_len

router = APIRouter()


@router.post("/beautify", response_model=EditResponse)
async def beautify_site(payload: EditRequest) -> EditResponse:
    client = OpenAIClientSingleton.get_client()

    html_len = safe_len(payload.html)
    comando_len = safe_len(payload.comando)

    modelo = escolher_modelo(
        task=CodexTask.BEAUTIFY,
        html_len=html_len,
        comando_len=comando_len,
    )

    prompt = f"""
Você é o Merse Codex — estilista de UI.

Objetivo:
- Melhorar APENAS a APARÊNCIA visual do HTML (spacing, fonts, cores, bordas, sombras, etc)
- Manter o conteúdo e estrutura lógica.
- Estilo: moderno, clean, um toque leve de Merse (cosmic, neon sutil).

Regras:
- NÃO explique o que fez.
- NÃO use markdown.
- Retorne APENAS o HTML final.

HTML:
{payload.html}

Comando opcional do usuário:
{payload.comando}
""".strip()

    try:
        completion = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Você é o Merse Codex, especialista em UI/UX."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar modelo: {e}")

    message = completion.choices[0].message.content or ""

    usage = getattr(completion, "usage", None)
    tokens_prompt = getattr(usage, "prompt_tokens", None) if usage else None
    tokens_resposta = getattr(usage, "completion_tokens", None) if usage else None
    tokens_total = getattr(usage, "total_tokens", None) if usage else None
    custo = estimar_custo_usd(tokens_total, modelo) if tokens_total else None

    return EditResponse(
        html_atualizado=message.strip(),
        tokens_usados_prompt=tokens_prompt,
        tokens_usados_resposta=tokens_resposta,
        modelo=modelo,
        custo_estimado_usd=custo,
    )