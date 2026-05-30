from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def invoke(
        self,
        prompt: str,
    ) -> str:
        pass
