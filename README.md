# pyplz

`pyplz` - a python-first, friction-free, task runner.

```bash
pip install pyplz
```

## Demo

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

!!! info "Dev Dependencies"

    Development dependencies (e.g., `pytest`) are best included in a dedicated file (e.g. `requirements.dev.txt`). Add `plz` to your dev dependencies to make it available in development, out of the box, for every project contributor.


### Example