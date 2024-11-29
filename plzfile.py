from pyplz import plz


@plz.task()
def lint():
    """Lint code"""
    plz.run("ruff check src/pyplz")


@plz.task()
def test():
    """Run tests"""
    plz.run("pytest")


@plz.task()
def test_coverage():
    """Run tests with coverage"""
    # execute tests with coverage
    plz.run("coverage run --source 'src/pyplz/' --omit '*/__pycache__/*' -m pytest")
    plz.run("coverage report -m --fail-under=95")


@plz.task(requires=[lint, test])
def validate():
    """Validate code (lint and test)"""
    plz.print("Validation successful")


@plz.task()
def doc():
    from scripts import doc_gen

    doc_gen.create_index_doc()
    plz.run("mkdocs build")


@plz.task(requires=doc)
def doc_serve():
    plz.run("mkdocs serve")
