from abc import ABC, abstractmethod


class CacheProvider(ABC):
    @abstractmethod
    def get(self, key: str) -> str | None:
        pass

    @abstractmethod
    def set(
        self,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        pass

    @abstractmethod
    def delete(
        self,
        key: str,
    ) -> None:
        pass
