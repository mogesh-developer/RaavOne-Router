from typing import Any

from .config import RouterConfig
from .exceptions import RouterLLMError
from .interfaces import (
    LLMProvider,
    MemoryProvider,
    ToolProvider,
)
from .models import Route, RouteType, RoutingResult


class RaavOneRouter:

    def __init__(
        self,
        llm: LLMProvider | None = None,
        memory: MemoryProvider | None = None,
        tools: ToolProvider | None = None,
        config: RouterConfig | None = None,
    ):
        self.llm = llm
        self.memory = memory
        self.tools = tools
        self.config = config or RouterConfig()

    # ── Public API ─────────────────────────────────────────────────────────────

    def route(self, message: str) -> Route:
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        result = self.route_all(message)

        if result.primary is None:
            return self._fallback("no_route")

        return result.primary

    async def aroute(self, message: str) -> Route:
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        result = await self.aroute_all(message)
        if result.primary is None:
            return self._fallback("no_route")
        return result.primary

    async def aroute_all(self, message: str) -> RoutingResult:
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        message = message.lower().strip()

        if not message:
            return RoutingResult(routes=[self._fallback("empty_message")])

        routes: list[Route] = []

        if self._is_memory_request(message):
            routes.append(self._create_route(
                RouteType.MEMORY,
                "memory",
                self.config.memory_confidence,
                "memory_query",
            ))

        tool_target = self._get_tool_target(message)
        if tool_target:
            routes.append(self._create_route(
                RouteType.TOOL,
                tool_target,
                self.config.tool_confidence,
                "tool_query",
            ))

        # LLM-assisted routing when no keyword rules matched
        if not routes and self.config.enable_llm_routing:
            llm_route = await self._aroute_with_llm(message)
            if llm_route:
                routes.append(llm_route)

        # Plain LLM fallback
        if not routes:
            routes.append(self._create_route(
                RouteType.LLM,
                "llm",
                self.config.llm_confidence,
                "general_query",
            ))

        routes.sort(key=lambda r: r.priority)
        return RoutingResult(routes=routes)

    def route_all(self, message: str) -> RoutingResult:
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        message = message.lower().strip()

        if not message:
            return RoutingResult(routes=[self._fallback("empty_message")])

        routes: list[Route] = []

        if self._is_memory_request(message):
            routes.append(self._create_route(
                RouteType.MEMORY,
                "memory",
                self.config.memory_confidence,
                "memory_query",
            ))

        tool_target = self._get_tool_target(message)
        if tool_target:
            routes.append(self._create_route(
                RouteType.TOOL,
                tool_target,
                self.config.tool_confidence,
                "tool_query",
            ))

        # LLM-assisted routing when no keyword rules matched
        if not routes and self.config.enable_llm_routing:
            llm_route = self._route_with_llm(message)
            if llm_route:
                routes.append(llm_route)

        # Plain LLM fallback
        if not routes:
            routes.append(self._create_route(
                RouteType.LLM,
                "llm",
                self.config.llm_confidence,
                "general_query",
            ))

        routes.sort(key=lambda r: r.priority)
        return RoutingResult(routes=routes)

    # ── Private helpers ────────────────────────────────────────────────────────

    def _create_route(
        self,
        route_type: RouteType,
        target: str,
        confidence: float,
        reason: str,
    ) -> Route:
        priority = self.config.route_priority.get(route_type.value, 99)
        if confidence < self.config.confidence_threshold:
            return self._fallback("low_confidence", confidence)
        return Route(
            type=route_type,
            target=target,
            confidence=confidence,
            priority=priority,
            metadata={"reason": reason},
        )

    def _fallback(self, reason: str, confidence: float = 0.0) -> Route:
        return Route(
            type=RouteType.FALLBACK,
            target="fallback",
            confidence=confidence,
            priority=self.config.route_priority.get("fallback", 99),
            metadata={"reason": reason},
        )

    def _route_with_llm(self, message: str) -> Route | None:
        if self.llm is None:
            return None

        try:
            result = self.llm.classify(message)
        except Exception as exc:
            raise RouterLLMError(
                f"LLM routing failed: {exc}"
            ) from exc

        if not isinstance(result, dict):
            raise RouterLLMError(
                "LLM classifier must return a dictionary."
            )

        route_type = result.get("type")
        target = result.get("target")
        confidence = result.get("confidence", 0.0)

        if not route_type or not target:
            raise RouterLLMError(
                "LLM response missing route type or target."
            )

        try:
            confidence = float(confidence)
            route_type = RouteType(route_type)
        except (ValueError, TypeError) as exc:
            raise RouterLLMError(
                "Invalid route returned by LLM."
            ) from exc

        return self._create_route(
            route_type,
            target,
            confidence,
            "llm_classification",
        )

    async def _aroute_with_llm(
        self,
        message: str,
    ) -> Route | None:
        if self.llm is None:
            return None

        try:
            result = self.llm.classify(message)
            if hasattr(result, "__await__"):
                result = await result
        except Exception as exc:
            raise RouterLLMError(
                f"LLM routing failed: {exc}"
            ) from exc

        if not isinstance(result, dict):
            raise RouterLLMError(
                "LLM classifier must return a dictionary."
            )

        route_type = result.get("type")
        target = result.get("target")
        confidence = result.get("confidence", 0.0)

        if not route_type or not target:
            raise RouterLLMError(
                "LLM response missing route type or target."
            )

        try:
            confidence = float(confidence)
            route_type = RouteType(route_type)
        except (ValueError, TypeError) as exc:
            raise RouterLLMError(
                "Invalid route returned by LLM."
            ) from exc

        return self._create_route(
            route_type,
            target,
            confidence,
            "llm_classification",
        )

    def _is_memory_request(self, message: str) -> bool:
        return any(kw in message for kw in self.config.memory_keywords)

    def _get_tool_target(self, message: str) -> str | None:
        for target, keywords in self.config.tool_keywords.items():
            if any(kw in message for kw in keywords):
                return target
        return None
