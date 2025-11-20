from pydantic import Field

from app.schemas.base import MerseBaseModel


class ExecuteRequest(MerseBaseModel):
    codigo: str = Field(..., description="Código ou conteúdo bruto que será transformado.")
    comando: str = Field(..., description="Instrução em linguagem natural para o Merse Codex.")
    linguagem: str | None = Field(
        default="auto",
        description="Linguagem alvo desejada (ex: html, react, tailwind). Use 'auto' para detecção automática.",
    )
