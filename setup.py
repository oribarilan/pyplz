from setuptools import setup, find_packages

setup(
    name="plz",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "plz=plz.app:main",
        ],
    },
    install_requires=[
        "typer",
    ],
)
