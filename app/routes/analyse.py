import json

from fastapi import APIRouter, HTTPException

from app.schemas.edit_request import EditRequest
from app.schemas.analyse_response import AnalyseResponse
from app.services.openai_client import OpenAIClientSingleton
from app.services.model_selector import CodexTask, escolher_modelo
from app.utils.cost import estimar_custo_usd
from app.utils.prompts import prompt_analyse_site
from app.utils.validate import safe_len

router = APIRouter()


@router.post("/analyse-site", response_model=AnalyseResponse)
async def analyse_site(payload: EditRequest) -> AnalyseResponse:
    client = OpenAIClientSingleton.get_client()

    html_len = safe_len(payload.html)
    modelo = escolher_modelo(
        task=CodexTask.ANALYSE,
        html_len=html_len,
        comando_len=0,
    )

    comando = (payload.comando or "analise este HTML").strip()
    prompt = prompt_analyse_site(payload.html, comando)

    try:
        completion = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Você é o Merse Codex, analisando um site profissionalmente."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar modelo: {e}")

    message = completion.choices[0].message.content or ""

    usage = getattr(completion, "usage", None)
    tokens_total = getattr(usage, "total_tokens", None) if usage else None
    custo = estimar_custo_usd(tokens_total, modelo) if tokens_total else None

    try:
        data = json.loads(message)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail=f"Resposta inválida do modelo: {exc}")

    return AnalyseResponse(
        qualidade_html=data.get("qualidade_html", ""),
        qualidade_css=data.get("qualidade_css", ""),
        sugestoes_melhoria=data.get("sugestoes_melhoria", []),
        problemas_detectados=data.get("problemas_detectados", []),
        nota_geral=float(data.get("nota_geral", 0.0)),
        modelo=modelo,
        tokens_usados=tokens_total,
        custo_estimado_usd=custo,
    )
