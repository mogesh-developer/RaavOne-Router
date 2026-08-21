<div align="center">

# RaavOne Router

### Lightweight, modular Python routing SDK for AI agents

<p>
  Multi-intent routing • Confidence scoring • Memory integration • Tool orchestration • Async workflows
</p>

<p>
  <a href="https://github.com/mogesh-developer/RaavOne-Router/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/mogesh-developer/RaavOne-Router?style=for-the-badge"></a>
  <a href="https://github.com/mogesh-developer/RaavOne-Router/network/members"><img alt="Forks" src="https://img.shields.io/github/forks/mogesh-developer/RaavOne-Router?style=for-the-badge"></a>
  <a href="https://github.com/mogesh-developer/RaavOne-Router/issues"><img alt="Issues" src="https://img.shields.io/github/issues/mogesh-developer/RaavOne-Router?style=for-the-badge"></a>
  <a href="https://github.com/mogesh-developer/RaavOne-Router/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/mogesh-developer/RaavOne-Router?style=for-the-badge"></a>
</p>

<p>
  <a href="#-overview">Overview</a> •
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-examples">Examples</a> •
  <a href="#-roadmap">Roadmap</a>
</p>

</div>

---

## 📌 Overview

**RaavOne Router** is built for developers creating modern AI agents that must intelligently route requests across LLMs, tools, memory, and fallback logic.

It focuses on three things:

- **Clarity** — predictable routing behavior
- **Modularity** — composable components and strategies
- **Scalability** — async-ready flow for production workloads

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 Multi-Intent Routing | Detect and handle one or more intents from a single request |
| 📊 Confidence Scoring | Score route quality and select the most reliable execution path |
| 🛠 Tool-Aware Dispatch | Route directly to tools/functions when needed |
| 💬 LLM Integration | Attach model-based handlers for generative reasoning |
| 🧾 Memory Context | Use short/long-term memory signals to improve intent decisions |
| ⚡ Async Workflows | Concurrent, non-blocking execution for high-throughput systems |
| 🧩 Modular Core | Plug in custom strategies, handlers, and policies easily |
| 🛡 Fallback Safety | Graceful fallback route for uncertain or unsupported intents |

---

## 🏗 Architecture

```text
┌─────────────────────────────────────────────┐
│                 User Input                  │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│         Intent + Context Analyzer           │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│                 Router Core                 │
│      (strategy + policy + orchestration)   │
└─────────────────────────────────────────────┘
          │               │               │
          ▼               ▼               ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Confidence     │ │ Memory Adapter │ │ Tool Resolver  │
│ Scoring Layer  │ │                │ │                │
└────────────────┘ └────────────────┘ └────────────────┘
          │               │               │
          └───────┬───────┴───────┬───────┘
                  ▼               ▼
          ┌─────────────────────────────────┐
          │         Route Selection         │
          └─────────────────────────────────┘
                  │
                  ▼
      ┌───────────────┬───────────────┬───────────────┐
      ▼               ▼               ▼               ▼
┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│ LLM       │   │ Tool      │   │ Memory    │   │ Fallback  │
│ Handler   │   │ Handler   │   │ Handler   │   │ Handler   │
└───────────┘   └───────────┘   └───────────┘   └───────────┘
```

---

## 📦 Installation

### 1) Clone repository

```bash
git clone https://github.com/mogesh-developer/RaavOne-Router.git
cd RaavOne-Router
```

### 2) Install dependencies

```bash
pip install -e .
```

### 3) (Optional) Dev setup

```bash
pip install -r requirements-dev.txt
```

> If your repo uses different dependency files, replace commands accordingly.

---

## 🚀 Quick Start

```python
from raavone_router import Router

router = Router(
    enable_memory=True,
    enable_tools=True,
    confidence_threshold=0.75
)

response = router.route(
    query="Summarize the report and extract action items",
    context={
        "user_role": "product_manager",
        "priority": "high"
    }
)

print("Intent:", response.intent)
print("Confidence:", response.confidence)
print("Output:", response.handler_output)
```

---

## 🔄 Async Example

```python
import asyncio
from raavone_router import Router

async def main():
    router = Router(enable_memory=True, enable_tools=True)

    result = await router.route_async(
        query="Find blockers and draft a project update",
        context={"team": "platform"}
    )

    print(result.intent, result.confidence)

asyncio.run(main())
```

---

## 🧪 Examples

### 1. Customer Support Agent
Route messages across:
- billing tool
- account policy lookup
- technical troubleshooting LLM flow

### 2. Productivity Copilot
Handle mixed requests:
- summarize notes (LLM)
- create tasks (tool)
- recall preferences (memory)

### 3. Multi-Step Operations
Pipeline:
- classify intent → score confidence → execute route → fallback if uncertain

---

## 🧱 Suggested Project Structure

```text
RaavOne-Router/
├─ raavone_router/
│  ├─ router.py
│  ├─ intents/
│  ├─ handlers/
│  ├─ scoring/
│  ├─ memory/
│  └─ tools/
├─ examples/
├─ tests/
├─ README.md
└─ pyproject.toml
```

---

## 📚 API Snapshot (Conceptual)

| Component | Purpose |
|---|---|
| `Router(...)` | Initialize router with strategy, thresholds, adapters |
| `route(query, context=None)` | Synchronous routing execution |
| `route_async(query, context=None)` | Async routing execution |
| `RouteResult.intent` | Predicted intent label(s) |
| `RouteResult.confidence` | Confidence score(s) |
| `RouteResult.handler_output` | Final execution output |
| `RouteResult.metadata` | Diagnostics, traces, route details |

> Adjust names according to your actual implementation.

---

## ✅ Best Practices

- Use a **confidence threshold** to reduce incorrect dispatches
- Keep handlers **single-purpose and testable**
- Add a robust **fallback route** for unknown intent
- Log route decisions for **observability and tuning**
- Prefer async execution in multi-request environments

---

## 🛣 Roadmap

- [ ] Strategy ensembles for hybrid routing
- [ ] Built-in tracing/telemetry integrations
- [ ] First-class provider adapters (OpenAI, Anthropic, etc.)
- [ ] Route performance benchmark toolkit
- [ ] Visual route debugging utilities

---

## 🤝 Contributing

Contributions are welcome and appreciated.

1. Fork this repository  
2. Create a feature branch  
3. Commit your changes with clear messages  
4. Open a pull request with context and tests

---

## 📄 License

This project is licensed under the terms defined in the [LICENSE](https://github.com/mogesh-developer/RaavOne-Router/blob/main/LICENSE) file.

---

## 💬 Support & Feedback

- Open an issue: https://github.com/mogesh-developer/RaavOne-Router/issues
- Share ideas for new routing strategies and integrations
- Star the project if you find it useful ⭐

---

<div align="center">
  Built for robust, production-ready AI agent orchestration.
</div>
