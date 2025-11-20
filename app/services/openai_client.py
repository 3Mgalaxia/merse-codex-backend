import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAIClientSingleton:
    _client: Optional[OpenAI] = None

    @classmethod
    def get_client(cls) -> OpenAI:
        if cls._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            project_id = os.getenv("OPENAI_PROJECT_ID")

            if not api_key:
                raise RuntimeError(
                    "Defina OPENAI_API_KEY no .env antes de iniciar o Merse Codex."
                )

            cls._client = OpenAI(
                api_key=api_key,
                project=project_id if project_id else None,
            )

        return cls._client