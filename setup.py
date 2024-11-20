from setuptools import setup, find_packages

setup(
    name="plz",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "typer",
    ],
    entry_points={
        "console_scripts": [
            "plz=plz_cli:app",
        ],
    },
)