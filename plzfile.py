from pyplz import plz


@plz.task()
def lint():
    """Lint code"""
    plz.run("ruff check")


@plz.task()
def test():
    """Run tests"""
    plz.run("pytest")


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
