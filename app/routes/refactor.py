import re
import json

from fastapi import APIRouter, HTTPException

from app.schemas.edit_request import EditRequest
from app.schemas.advanced_response import RefactorResponse
from app.services.openai_client import OpenAIClientSingleton
from app.services.model_selector import CodexTask, escolher_modelo
from app.utils.cost import estimar_custo_usd
from app.utils.prompts import prompt_refactor
from app.utils.validate import safe_len

router = APIRouter()


def separar_html_e_json(resposta: str) -> tuple[str, list[str]]:
    """
    Separa bloco de HTML e JSON do formato:

    HTML:
    ...html...

    JSON:
    { "melhorias_aplicadas": [...] }
    """
    html_parte = ""
    melhorias = []

    match_html = re.search(r"HTML:\s*(.*?)\s*JSON:", resposta, re.DOTALL | re.IGNORECASE)
    if match_html:
        html_parte = match_html.group(1).strip()
        json_parte = resposta[match_html.end():].strip()
    else:
        html_parte = resposta.strip()
        json_parte = ""

    if json_parte:
        try:
            data = json.loads(json_parte)
            melhorias = data.get("melhorias_aplicadas", [])
        except json.JSONDecodeError:
            melhorias = []

    return html_parte, melhorias


@router.post("/refactor", response_model=RefactorResponse)
async def refactor_site(payload: EditRequest) -> RefactorResponse:
    client = OpenAIClientSingleton.get_client()

    html_len = safe_len(payload.html)
    comando_len = safe_len(payload.comando)

    modelo = escolher_modelo(
        task=CodexTask.REFACTOR,
        html_len=html_len,
        comando_len=comando_len,
    )

    prompt = prompt_refactor(payload.html, payload.comando)

    try:
        completion = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Você é o Merse Codex, refatorando HTML para nível profissional."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar modelo: {e}")

    message = completion.choices[0].message.content or ""
    html_refatorado, melhorias = separar_html_e_json(message)

    usage = getattr(completion, "usage", None)
    tokens_total = getattr(usage, "total_tokens", None) if usage else None
    custo = estimar_custo_usd(tokens_total, modelo) if tokens_total else None

    return RefactorResponse(
        html_refatorado=html_refatorado,
        melhorias_aplicadas=melhorias,
        modelo=modelo,
        tokens_usados=tokens_total,
        custo_estimado_usd=custo,
    )