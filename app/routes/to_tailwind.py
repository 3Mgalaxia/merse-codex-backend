from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), project=os.getenv("OPENAI_PROJECT_ID"))

class TailwindRequest(BaseModel):
    html: str

class TailwindResponse(BaseModel):
    html: str
    modelo: str | None = None

@router.post("/to-tailwind", response_model=TailwindResponse)
async def to_tailwind(payload: TailwindRequest):

    prompt = f"""
Converta o HTML abaixo para TAILWIND CSS.
Regra:
- NADA de markdown
- Retorne APENAS o HTML
- Nada de explicações
- Preserve o conteúdo, apenas converta o estilo

HTML:
{payload.html}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    message = completion.choices[0].message.content

    return TailwindResponse(html=message.strip(), modelo=completion.model)