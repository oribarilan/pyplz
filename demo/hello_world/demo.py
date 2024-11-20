from plz import Plz

app = Plz()

@app.task("hello")
def hello():
    """Print 'hello world'."""
    print("hello world")