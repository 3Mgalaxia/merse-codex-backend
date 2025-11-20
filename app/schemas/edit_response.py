from typing import Optional

from app.schemas.base import MerseBaseModel


class EditResponse(MerseBaseModel):
    html_atualizado: str
    tokens_usados_prompt: Optional[int] = None
    tokens_usados_resposta: Optional[int] = None
    modelo: Optional[str] = None
    custo_estimado_usd: Optional[float] = None