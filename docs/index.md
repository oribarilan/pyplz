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
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - On macOS and Linux: `source .venv/bin/activate`
   - On Windows: `.venv\Scripts\activate`
4. Upgrade pip: `pip install --upgrade pip`
5. Install dependencies: `pip install -r requirements.dev.txt`
6. In the root directory: `pip install -e .`

## Features

[x] List with plz -l (and default)
[x] Default
[x] Help flags (-h and --help)
[x] dependencies - single, list, with or without args
[x] plz -h
[x] running commands
[ ] environment variables
    [x] .env file
    [ ] task definition
    [x] in-line
    [ ] plz scope (in config)
[ ] verbosity level
    [ ] verbose loading env variables

### Backlog Should
[x] move to toml based setup
[x] arguments (support from command line and in docs)
[x] test Task
[x] test run_task
[x] test main help
[x] test task help
[x] test dependencies
[ ] test coverage
[ ] CI with test
[ ] CI with test coverage
[ ] CD
[ ] doc pages
[ ] load specific file
[ ] heirachial loading

### Could
[ ] order commands
[ ] `plz .create-demo`
[ ] async commands
[ ] `plz.progress`
[ ] support options for commands
[ ] use argparse lib
[ ] "Did you mean?" offer another command if something resembles it.