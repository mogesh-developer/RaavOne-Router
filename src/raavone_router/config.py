from dataclasses import dataclass, field


@dataclass
class RouterConfig:
    confidence_threshold: float = 0.50

    memory_confidence: float = 0.90
    tool_confidence: float = 0.90
    llm_confidence: float = 0.80

    enable_llm_routing: bool = False

    route_priority: dict[str, int] = field(default_factory=lambda:{
        "memory": 1,
        "tool": 2,
        "llm": 3,
        "direct":4,
        "fallback": 5
    })

    memory_keywords: list[str] = field(default_factory=lambda: [
        "remember",
        "previous conversation",
        "what did i say",
        "memory",
    ])

    tool_keywords: dict[str, list[str]] = field(default_factory=lambda: {
        "weather": [
            "weather",
            "temperature",
            "forecast",
        ],
        "calculator": [
            "calculate",
            "calculator",
            "compute",
        ],
        "web_search": [
            "search",
            "google",
            "find online",
        ],
        "open": [
            "open",
            "launch",
        ],
        "messaging": [
            "send",
            "message",
            "email",
        ],
    })

    def __post_init__(self):
        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError(
                "confidence_threshold must be between 0 and 1"
            )

        if not 0.0 <= self.memory_confidence <= 1.0:
            raise ValueError(
                "memory_confidence must be between 0 and 1"
            )

        if not 0.0 <= self.tool_confidence <= 1.0:
            raise ValueError(
                "tool_confidence must be between 0 and 1"
            )

        if not 0.0 <= self.llm_confidence <= 1.0:
            raise ValueError(
                "llm_confidence must be between 0 and 1"
            )