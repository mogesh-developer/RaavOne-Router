# RaavOne-Router

Lightweight, configurable intent router and multi-intent dispatcher for RaavOne Python applications.

## Features

- 🎯 **Intent Routing**: Classifies user queries into `MEMORY`, `TOOL`, `LLM`, or `FALLBACK` routes.
- 🔀 **Multi-Intent Support**: Detect multiple user intents in a single message with `route_all()` and `aroute_all()`.
- ⚡ **Sync & Async API**: Seamless support for both synchronous and `asyncio` workflows (`route`, `aroute`, `route_all`, `aroute_all`).
- ⚙️ **Configurable Keywords & Confidence**: Easily adjust keyword rules, confidence thresholds, and priority ordering via `RouterConfig`.
- 🤖 **LLM-Assisted Routing**: Optional fallback to LLM classification when keyword rules do not match.
- 🔌 **Decoupled Architecture**: Clean protocol interfaces (`LLMProvider`, `MemoryProvider`, `ToolProvider`, `RouteExecutor`) with zero tight coupling.

## Installation

```bash
pip install -e .
```

## Quickstart

### Basic Single Intent Routing

```python
from raavone_router import RaavOneRouter

router = RaavOneRouter()

# Single route
route = router.route("What is the weather today?")
print(route.type)    # RouteType.TOOL
print(route.target)  # weather
```

### Multi-Intent Routing

```python
from raavone_router import RaavOneRouter

router = RaavOneRouter()

# Multi-intent routing
result = router.route_all("Remember my name and search the weather")

for route in result.routes:
    print(route.type, route.target, route.priority)
# Output:
# RouteType.MEMORY memory 1
# RouteType.TOOL weather 2
```

### Custom Configuration

```python
from raavone_router import RaavOneRouter, RouterConfig

config = RouterConfig(
    confidence_threshold=0.6,
    tool_keywords={
        "weather": ["weather", "climate"],
        "calculator": ["calculate", "math", "solve"],
    }
)

router = RaavOneRouter(config=config)
route = router.route("Can you solve this math problem?")
print(route.target)  # calculator
```

### Async Usage

```python
import asyncio
from raavone_router import RaavOneRouter

async def main():
    router = RaavOneRouter()
    routing = await router.aroute_all("Remember my name and search the weather")
    print([r.target for r in routing.routes])

asyncio.run(main())
```

## License

MIT
