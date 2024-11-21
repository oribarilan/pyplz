from setuptools import setup, find_packages

setup(
    name="plz",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        # Add any dependencies here
    ],
)