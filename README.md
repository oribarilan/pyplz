# plz

`plz` is a python-first command runner.
`plz` allows you to define commands in python, and run them from the command line.
No more bash scripts, makefiles or copy pasting commands from the docs.

`plz` can be used for many things, but it is especially useful for python projects, as no other installation is required.

## Installation
1. Using python 3.9 or later, run `pip install plz`
2. Create a `plzfile.py` in the root of your project
3. Using your terminal, execute `plz` in the root of your project

> **Note:** Development dependencies are best included in a `requirements.dev.txt` file, and installed with `pip install -r requirements.dev.txt`. Add `plz` to your `requirements.dev.txt` file to make it available in development, out of the box.

## Usage

## Contribution

### Installation

1. Python 3.9
2. `python -m venv .venv`
3. `source .venv/bin/activate`
4. `pip install --upgrade pip`
5. `pip install -r requirements.txt -r requirements.dev.txt`
6. in the root dir: `pip install -e .`

## Features

[ ] List with plz -l (and default)
[x] Default
[x] Help flags (-h and --help)
[x] dependencies - list or single
[ ] plz help (general help that is configurable)

### Backlog Should
[ ] arguments (support from command line and in docs)
[ ] dependencies - list or single, with arguments
[ ] env variables and .env file
[ ] doc pages
[ ] tests
[ ] move to toml based setup

### Could
[ ] order commands
[ ] `plz .create-demo`
[ ] async commands
[ ] `plz.progress`
[ ] support options for commands