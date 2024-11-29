from enum import Enum

from pyplz import plz


class Coffee(Enum):
    """Coffee enum"""

    ESPRESSO = "espresso"
    DOUBLE_ESPRESSO = "double espresso"


@plz.task()
def lint():
    plz.run("linting...")


@plz.task()
def test():
    plz.run("testing...")


@plz.task()
def echo(*args):
    """Echo message"""
    plz.run(f"echo {' '.join(args)}")


@plz.task(envs={"a": "1"})
def echo2():
    plz.run("echo $a")


@plz.task()
def drink_coffee(type: Coffee = Coffee.ESPRESSO):
    """Brew coffee"""
    plz.print(f"Drinking {type.value}")


@plz.task()
def a(num: int = 1):
    plz.print(f"a + {num}")


@plz.task(requires=[(a, (2,))])
def b(num: int = 2):
    plz.print(f"b + {num}")


@plz.task(requires=[(a, (3,)), (b, (4,))])
def c(num: int):
    plz.print(f"c + {num}")


@plz.task()
def doc():
    from scripts import doc_gen

    doc_gen.create_index_doc()
    plz.run("mkdocs build")


@plz.task(requires=doc)
def doc_serve():
    plz.run("mkdocs serve")
