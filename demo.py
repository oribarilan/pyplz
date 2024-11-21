from plz import Plz

plz = Plz()


@plz.task("hello")
def hello():
    """Print 'hello world'."""
    print("hello world")
