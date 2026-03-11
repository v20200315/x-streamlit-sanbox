import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


@dataclass
class OpenAIConfig:
    api_key: str
    model: str

    @classmethod
    def from_env(cls) -> 'OpenAIConfig':
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise RuntimeError('OPENAI_API_KEY is not set in environment or .env')

        model = os.getenv('OPENAI_MODEL', 'gpt-4.1-mini')
        return cls(api_key=api_key, model=model)


openai_config = OpenAIConfig.from_env()
