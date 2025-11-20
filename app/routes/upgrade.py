from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), project=os.getenv("OPENAI_PROJECT_ID"))

class UpgradeRequest(BaseModel):
    html: str

class UpgradeResponse(BaseModel):
    html_melhorado: str
    modelo: str | None = None

@router.post("/upgrade", response_model=UpgradeResponse)
async def upgrade(payload: UpgradeRequest):

    prompt = f"""
Melhore completamente o HTML abaixo no estilo MERSE:
- mais bonito
- mais profissional
- mais moderno
- responsivo
- sem markdown
- retorne só HTML

HTML:
{payload.html}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    html = completion.choices[0].message.content.strip()

    return UpgradeResponse(html_melhorado=html, modelo=completion.model)