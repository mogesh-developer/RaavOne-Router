from typing import Any, Protocol

from .models import (
    ExecutionResult,
    Route,
    RoutingResult,
)


class RouteExecutor(Protocol):

    def execute(self, route: Route) -> Any:
        ...

    async def aexecute(self, route: Route) -> Any:
        ...

    def execute_all(
        self,
        routing: RoutingResult,
    ) -> list[ExecutionResult]:
        ...

    async def aexecute_all(
        self,
        routing: RoutingResult,
    ) -> list[ExecutionResult]:
        ...