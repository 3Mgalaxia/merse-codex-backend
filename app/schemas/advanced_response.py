from typing import List, Optional

from app.schemas.base import MerseBaseModel


class RefactorResponse(MerseBaseModel):
    html_refatorado: str
    melhorias_aplicadas: List[str]
    modelo: str
    tokens_usados: Optional[int] = None
    custo_estimado_usd: Optional[float] = None