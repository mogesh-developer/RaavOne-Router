from typing import Any, Protocol


class LLMProvider(Protocol):

    def classify(self, message: str) -> dict[str, Any]:
        ...


class MemoryProvider(Protocol):

    def search(self, query: str) -> Any:
        ...


class ToolProvider(Protocol):

    def has_tool(self, name: str) -> bool:
        ...

    def get_tool(self, name: str) -> Any:
        ...