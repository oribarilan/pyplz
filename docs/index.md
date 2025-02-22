#  <img src="assets/please.png" alt="drawing" width="40" height="40"/> pyplz

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

`pyplz` aims to be a friction-free task runner. While many task runners simplify development, they can also add friction with unfamiliar syntax, extra tools, or difficult integrations.

🐍 **Python-first**: Leverage familiar Python syntax—if you know Python, you know `pyplz`.  
🤗 **Author-friendly**: Intuitive and ready to use out of the box, with built-in support for development & debugging.  
💻 **CLI-compliant**: Enjoy a command-line interface that adheres to GNU and POSIX conventions, ensuring a seamless terminal experience.
🔗 **Integration-ready**: Whether you're running Python locally, in containers, or in a CI/CD pipeline, `pyplz` fits seamlessly into your environment.  
📚 **Documented**: Access extensive documentation and automatically generated task-specific help, ensuring you always have the information you need.

## Getting Started

### Installation
1. Using python 3.9 or later, run `pip install pyplz`
2. Create a `plzfile.py` in the root of your project
3. Using your terminal, execute `plz` in the root of your project

!!! tip "Development Dependencies"
    For best practice, include development dependencies (e.g., `pytest`) in a dedicated file (such as `requirements.dev.txt`). Add `pyplz` to your dev dependencies to ensure it's available out of the box for every project contributor.


### Example