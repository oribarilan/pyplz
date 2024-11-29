# Command Execution (Run)

TODO - link to the run API

`run` is the most basic function in `plz` and is used to run any terminal command.

Run has many different options and flags to help you run your commands in the way you want.
You can refrence the API documentation for more information, or explore the function documentation in-code.

For now, here is a simple example of how to use `run`:

```python
@plz.task()
def my_task():
    # Run any terminal command
    plz.run("echo Hello, World!")
```