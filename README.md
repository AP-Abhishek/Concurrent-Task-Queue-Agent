# Concurrent Task Queue

An intelligent task-processing agent designed to fetch and execute asynchronous workloads from public sources. It utilizes robust content inspection and an external API to filter out unsafe instructions. The execution engine handles multiple tasks concurrently, employing strict concurrency controls to guarantee that shared resources—such as counters and databases—remain perfectly consistent and free from race conditions, even under adversarial timing.

## Key Features

* **Zero Data Corruption:** Uses `asyncio.Lock()` to process concurrent reads/writes atomically, preventing race conditions.
* **Dynamic Validation:** Automatically tallies approved tasks and asserts them against the final state count, mathematically proving that no updates were lost.
* **Security & Reasoning:** Uses local Regex to block prompt injections/RCE, and queries the free Cloudflare DNS API to drop tasks targeting non-existent domains.
* **Modern Stack:** Built with `asyncio` for concurrency, `httpx` for fast async networking, and managed entirely via `uv`.

## Quick Start

This project is built using **[uv](https://github.com/astral-sh/uv)** for lightning-fast dependency management.

**1. Clone the repository**

```bash
git clone https://github.com/AP-Abhishek/Concurrent-Task-Queue-Agent.git
cd Concurrent-Task-Queue-Agent
```

**2. Install dependencies**

```bash
uv sync
```

**3. Run the Agent**

```bash
uv run main.py
```
