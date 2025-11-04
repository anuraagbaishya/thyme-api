from abc import ABC, abstractmethod

from google import genai


class AiTask(ABC):
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.model = model

    @abstractmethod
    def prompt():
        pass

    @abstractmethod
    def ai_request():
        pass
