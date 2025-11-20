from pydantic import Field
from app.schemas.base import MerseBaseModel


class EditRequest(MerseBaseModel):
    html: str = Field(..., description="HTML atual do site do usuário.")
    comando: str | None = Field(
        default=None,
        description="Comando em linguagem natural para editar o site.",
        examples=["Troque o título para Merse e deixe o fundo escuro neon."],
    )
