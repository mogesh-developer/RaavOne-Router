import pytest

from raavone_router import __version__, RaavOneRouter, RouteType, RoutingResult
from raavone_router.config import RouterConfig
from raavone_router.exceptions import RouterLLMError
from raavone_router.models import ExecutionResult


def test_package_version():
    assert __version__ == "1.0.0"


# ── Core routing ───────────────────────────────────────────────────────────────

def test_empty_message():
    router = RaavOneRouter()
    result = router.route("")
    assert result.type == RouteType.FALLBACK
    assert result.target == "fallback"
    assert result.metadata["reason"] == "empty_message"


def test_memory_route():
    router = RaavOneRouter()
    result = router.route("Do you remember what I said earlier?")
    assert result.type == RouteType.MEMORY
    assert result.target == "memory"
    assert result.confidence == 0.90


def test_tool_route_weather():
    router = RaavOneRouter()
    result = router.route("What is the weather today?")
    assert result.type == RouteType.TOOL
    assert result.target == "weather"


def test_tool_route_calculator():
    router = RaavOneRouter()
    result = router.route("Can you calculate 5 + 3?")
    assert result.type == RouteType.TOOL
    assert result.target == "calculator"


def test_tool_route_web_search():
    router = RaavOneRouter()
    result = router.route("Search for the best Python tutorials")
    assert result.type == RouteType.TOOL
    assert result.target == "web_search"


def test_tool_route_open():
    router = RaavOneRouter()
    result = router.route("Open Chrome browser")
    assert result.type == RouteType.TOOL
    assert result.target == "open"


def test_llm_fallback():
    router = RaavOneRouter()
    result = router.route("Tell me a story about a dragon")
    assert result.type == RouteType.LLM
    assert result.target == "llm"
    assert result.confidence == 0.80


# ── Configurable routing ───────────────────────────────────────────────────────

def test_custom_tool_keywords():
    config = RouterConfig(
        tool_keywords={
            "calculator": [
                "math",
                "solve",
            ]
        }
    )
    router = RaavOneRouter(config=config)
    result = router.route("Can you solve this problem?")
    assert result.type == RouteType.TOOL
    assert result.target == "calculator"


# ── RoutingResult / multi-intent ───────────────────────────────────────────────

def test_primary_route():
    router = RaavOneRouter()
    result = router.route_all("What is the weather today?")
    assert isinstance(result, RoutingResult)
    assert result.primary is not None
    assert result.primary.type == RouteType.TOOL
    assert result.primary.target == "weather"


def test_multi_intent_routing():
    router = RaavOneRouter()

    result = router.route_all(
        "Remember my name and search the weather"
    )

    assert len(result.routes) == 2

    assert result.routes[0].type == RouteType.MEMORY
    assert result.routes[0].target == "memory"

    assert result.routes[1].type == RouteType.TOOL
    assert result.routes[1].target == "weather"


# ── Priority routing ───────────────────────────────────────────────────────────

def test_route_priority():
    router = RaavOneRouter()

    result = router.route_all(
        "Remember my name and search the weather"
    )

    assert len(result.routes) == 2

    assert result.routes[0].type == RouteType.MEMORY
    assert result.routes[0].priority == 1

    assert result.routes[1].type == RouteType.TOOL
    assert result.routes[1].priority == 2


# ── LLM-assisted routing ───────────────────────────────────────────────────────

def test_llm_routing_disabled_by_default():
    """enable_llm_routing=False → plain LLM fallback, no LLM.classify call."""
    router = RaavOneRouter()
    assert router.config.enable_llm_routing is False

    result = router.route("Something completely unknown")
    assert result.type == RouteType.LLM


def test_llm_routing_skipped_when_no_llm_injected():
    """enable_llm_routing=True but no LLM injected → still falls back to LLM."""
    config = RouterConfig(enable_llm_routing=True)
    router = RaavOneRouter(config=config)

    result = router.route("Something completely unknown")
    assert result.type == RouteType.LLM


def test_llm_routing_used_when_enabled():
    """enable_llm_routing=True + LLM injected → _route_with_llm() is called."""

    class MockLLM:
        def classify(self, message: str) -> dict:
            return {
                "type": "tool",
                "target": "calculator",
                "confidence": 0.85,
            }

    config = RouterConfig(enable_llm_routing=True)
    router = RaavOneRouter(llm=MockLLM(), config=config)

    result = router.route("Do the maths")
    assert result.type == RouteType.TOOL
    assert result.target == "calculator"
    assert result.confidence == 0.85


class BrokenLLM:
    def classify(self, message: str):
        raise RuntimeError("LLM unavailable")


def test_llm_error():
    config = RouterConfig(
        enable_llm_routing=True
    )
    router = RaavOneRouter(
        llm=BrokenLLM(),
        config=config,
    )
    with pytest.raises(RouterLLMError):
        router.route(
            "Tell me about the sky conditions"
        )


@pytest.mark.asyncio
async def test_async_router():
    router = RaavOneRouter()

    result = await router.aroute(
        "What is the weather today?"
    )

    assert result.type == RouteType.TOOL
    assert result.target == "weather"


@pytest.mark.asyncio
async def test_async_multi_intent():
    router = RaavOneRouter()

    result = await router.aroute_all(
        "Remember my name and search the weather"
    )

    assert len(result.routes) == 2
    assert result.routes[0].type == RouteType.MEMORY
    assert result.routes[1].type == RouteType.TOOL


# ── Input validation ───────────────────────────────────────────────────────────

def test_none_message():
    router = RaavOneRouter()

    with pytest.raises(TypeError):
        router.route(None)


def test_numeric_message():
    router = RaavOneRouter()

    with pytest.raises(TypeError):
        router.route(12345)


def test_whitespace_message():
    router = RaavOneRouter()

    result = router.route("     ")

    assert result.type == RouteType.FALLBACK
    assert result.target == "fallback"


@pytest.mark.asyncio
async def test_async_invalid_message():
    router = RaavOneRouter()

    with pytest.raises(TypeError):
        await router.aroute(None)


# ── Config validation ──────────────────────────────────────────────────────────

def test_invalid_confidence_threshold():
    with pytest.raises(ValueError):
        RouterConfig(
            confidence_threshold=1.5
        )


# ── Provider injection contract ────────────────────────────────────────────────

class FakeLLM:
    def classify(self, message: str):
        return {
            "type": "tool",
            "target": "weather",
            "confidence": 0.95,
        }


class FakeMemory:
    def search(self, query: str):
        return []


class FakeTools:
    def has_tool(self, name: str):
        return name == "weather"

    def get_tool(self, name: str):
        return None


def test_provider_injection():
    router = RaavOneRouter(
        llm=FakeLLM(),
        memory=FakeMemory(),
        tools=FakeTools(),
    )

    assert router.llm is not None
    assert router.memory is not None
    assert router.tools is not None

def test_execution_result():
    router = RaavOneRouter()

    route = router.route("What is the weather?")

    result = ExecutionResult(
        success=True,
        result="Sunny",
        route=route,
    )

    assert result.success is True
    assert result.result == "Sunny"
    assert result.route == route


# ── Integration tests (Router + Executor flow) ────────────────────────────────

class FakeExecutor:
    def execute_all(self, routing):
        return [
            ExecutionResult(
                success=True,
                result=f"executed:{route.target}",
                route=route,
            )
            for route in routing.routes
        ]

    async def aexecute_all(self, routing):
        return self.execute_all(routing)


def test_router_executor_flow():
    router = RaavOneRouter()
    executor = FakeExecutor()

    routing = router.route_all(
        "Remember my name and search the weather"
    )

    results = executor.execute_all(routing)

    assert len(results) == 2

    assert results[0].success is True
    assert results[0].route.target == "memory"

    assert results[1].success is True
    assert results[1].route.target == "weather"


@pytest.mark.asyncio
async def test_async_router_executor_flow():
    router = RaavOneRouter()
    executor = FakeExecutor()

    routing = await router.aroute_all(
        "Remember my name and search the weather"
    )

    results = await executor.aexecute_all(routing)

    assert len(results) == 2

    assert results[0].route.target == "memory"
    assert results[1].route.target == "weather"