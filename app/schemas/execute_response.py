from typing import Optional

from app.schemas.base import MerseBaseModel


class ExecuteResponse(MerseBaseModel):
    sucesso: bool = True
    resultado: str
    modelo: Optional[str] = None
    tokens_usados: Optional[int] = None
    custo_estimado_usd: Optional[float] = None
