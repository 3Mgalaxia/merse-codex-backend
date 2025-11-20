from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), project=os.getenv("OPENAI_PROJECT_ID"))

class FixRequest(BaseModel):
    html: str

class FixResponse(BaseModel):
    html_corrigido: str
    problemas: list
    modelo: str | None = None

@router.post("/fix-errors", response_model=FixResponse)
async def fix_errors(payload: FixRequest):

    prompt = f"""
Analise o HTML abaixo, detecte problemas e retorne:
1. HTML corrigido
2. Lista de problemas em JSON

Formato:
{{
"html": "",
"problemas": []
}}

HTML:
{payload.html}
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    data = eval(completion.choices[0].message.content.strip())

    return FixResponse(
        html_corrigido=data["html"],
        problemas=data["problemas"],
        modelo=completion.model,
    )