from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RouteType(str, Enum):
    LLM = "llm"
    MEMORY = "memory"
    TOOL = "tool"
    DIRECT = "direct"
    FALLBACK = "fallback"


@dataclass
class Route:
    type: RouteType
    target: str
    confidence: float = 1.0
    priority: int = 99
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RoutingResult:
    routes: list[Route] = field(default_factory=list)

    @property
    def primary(self) -> Route | None:
        return self.routes[0] if self.routes else None


@dataclass
class ExecutionResult:
    success: bool
    result: Any = None
    error: str | None = None
    route: Route | None = None