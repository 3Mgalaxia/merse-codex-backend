from fastapi import APIRouter, HTTPException

from app.schemas.execute_request import ExecuteRequest
from app.schemas.execute_response import ExecuteResponse
from app.services.codex_engine import CodexEngine
from app.services.model_selector import CodexTask, escolher_modelo
from app.utils.cost import estimar_custo_usd
from app.utils.prompts import prompt_execute
from app.utils.validate import safe_len

router = APIRouter()


@router.post("/execute", response_model=ExecuteResponse)
async def execute_codex(payload: ExecuteRequest) -> ExecuteResponse:
    codigo_len = safe_len(payload.codigo)
    comando_len = safe_len(payload.comando)

    modelo = escolher_modelo(
        task=CodexTask.EXECUTE,
        html_len=codigo_len,
        comando_len=comando_len,
    )

    _, system_prompt, user_prompt = prompt_execute(payload.codigo, payload.comando, payload.linguagem)

    try:
        completion = CodexEngine.run(
            model=modelo,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.25,
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro ao executar comando no Codex: {error}")

    message = completion.content or payload.codigo
    tokens_total = completion.total_tokens
    custo = estimar_custo_usd(tokens_total, modelo) if tokens_total else None

    return ExecuteResponse(
        sucesso=True,
        resultado=message.strip(),
        modelo=modelo,
        tokens_usados=tokens_total,
        custo_estimado_usd=custo,
    )
