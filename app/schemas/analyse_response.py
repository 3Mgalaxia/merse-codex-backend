from typing import List, Optional

from app.schemas.base import MerseBaseModel


class AnalyseResponse(MerseBaseModel):
    qualidade_html: str
    qualidade_css: str
    sugestoes_melhoria: List[str]
    problemas_detectados: List[str]
    nota_geral: float
    modelo: str
    tokens_usados: Optional[int] = None
    custo_estimado_usd: Optional[float] = None