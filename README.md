#  <img src="docs/assets/please.png" alt="drawing" width="40" height="40"/> pyplz

Python-first Friction-free Task Runner.

⚠️ Please note ⚠️

`pyplz` is currently in early development. While it is already usable, some features are still missing, incomplete or not fully documented. Feel free to open an issue if you have any feedback or suggestions.

[//]: # (bages using https://shields.io/badges/)
[![build](https://img.shields.io/github/actions/workflow/status/oribarilan/plz/package_build.yml)](https://github.com/oribarilan/plz/actions/workflows/package_build.yml) [![coverage](https://img.shields.io/github/actions/workflow/status/oribarilan/plz/coverage.yml?label=coverage%3E95%25)](https://github.com/oribarilan/plz/actions/workflows/coverage.yml)

[![Python Versions](https://img.shields.io/badge/python-3.8|3.9|3.10|3.11|3.12-blue)](https://www.python.org/downloads/) [![PyPI - Version](https://img.shields.io/pypi/v/pyplz?color=1E7FBF)](https://pypi.org/project/pyplz/) [![Downloads](https://img.shields.io/pypi/dm/pyplz?color=1E7FBF)](https://pypi.org/project/pyplz/)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

```bash
pip install pyplz
```

## Why use a task runner?
A task runner automates tasks like building, testing, and deploying, making them
faster and more reliable. It ensures consistent execution and simplifies collaboration
 by providing clear, reusable commands.

## Why `pyplz`?

`pyplz` aims to be a friction-free task runner. While task runners simplify development, they often add friction with new syntax, extra tools, or integration issues.

1. **Python-first**: Familiar syntax, flexible, and powerful. If you know Python, you know `pyplz`.
2. **Simplicity**: Common features are built-in and work out of the box. No need for hafty configuration or tinkering.
3. **Integration**: If it can run Python, it can run `pyplz`. Use it in your project's dev environment, container, CI/CD, or anywhere else.
4. **Documentation**: `pyplz` offers extensive docs as well as generates task-specific help documentation, ensuring clarity and ease of use.

## Getting Started

### Installation
1. Using python 3.9 or later, run `pip install pyplz`
2. Create a `plzfile.py` in the root of your project
3. Using your terminal, execute `plz` in the root of your project

> Development dependencies (e.g., `pytest`) are best included in a dedicated file (e.g. `requirements.dev.txt`). Add `plz` to your dev dependencies to make it available in development, out of the box, for every project contributor.


### Example