from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), project=os.getenv("OPENAI_PROJECT_ID"))

class NextRequest(BaseModel):
    html: str

class NextResponse(BaseModel):
    component: str
    modelo: str | None = None

@router.post("/to-nextjs", response_model=NextResponse)
async def to_nextjs(payload: NextRequest):

    prompt = f"""
Converta o HTML abaixo em um componente React/Next.js funcional e moderno.
- Use função (export default function)
- Sem markdown
- Apenas o código final
- Converter inline para Tailwind

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

    code = completion.choices[0].message.content.strip()

    return NextResponse(component=code, modelo=completion.model)