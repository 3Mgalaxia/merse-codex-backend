from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), project=os.getenv("OPENAI_PROJECT_ID"))

class RefactorRequest(BaseModel):
    html: str
    comando: str | None = None

class RefactorResponse(BaseModel):
    html: str
    modelo: str | None = None
    tokens: int | None = None

@router.post("/refactor-ui", response_model=RefactorResponse)
async def refactor_ui(payload: RefactorRequest):

    comando = payload.comando or "Melhore o design visual no estilo MERSE."

    prompt = f"""
Você é o Merse Codex — especialista em melhorar o design visual de sites.

Aplique:
- visual moderno e premium
- cores suaves, neon elegante, bordas limpas
- melhor tipografia
- hierarquia clara
- sem comentários
- SEM markdown
- retorne apenas o novo HTML

HTML atual:
{payload.html}

Comando do usuário:
{comando}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    message = completion.choices[0].message.content

    return RefactorResponse(
        html=message.strip(),
        modelo=completion.model,
        tokens=completion.usage.total_tokens if completion.usage else None,
    )