from dataclasses import dataclass
from typing import Optional

from app.services.openai_client import OpenAIClientSingleton


@dataclass(slots=True)
class CodexCompletion:
    """Pequeno DTO com o resultado bruto da OpenAI."""

    content: str
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class CodexEngine:
    """
    Camada mínima para conversar com o cliente da OpenAI.
    Os handlers só precisam se preocupar com prompt e pós-processamento.
    """

    @staticmethod
    def run(
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
    ) -> CodexCompletion:
        client = OpenAIClientSingleton.get_client()

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )

        usage = getattr(completion, "usage", None)

        return CodexCompletion(
            content=(completion.choices[0].message.content or "").strip(),
            prompt_tokens=getattr(usage, "prompt_tokens", None) if usage else None,
            completion_tokens=getattr(usage, "completion_tokens", None) if usage else None,
            total_tokens=getattr(usage, "total_tokens", None) if usage else None,
        )
