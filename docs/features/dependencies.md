# Dependencies

Tasks can depend on other tasks. This is useful when one or more tasks a required to run before another task. 

For example, you may have a `lint` task that lints your code, and another `test` task that runs your tests.
Then, you may want to have a third `validate` task that will run `lint` and `test`.

This can look like this:

```python
@plz.task()
def lint():
    plz.run("ruff")

@plz.task()
def test():
    plz.run("pytest")

@plz.task(requires=[lint, test])
def validate():
    plz.print("validation successful")
```

Task dependencies can be defined in a few ways:
1. A single task `@plz.task(requires=lint)`
2. A list of tasks or tasks with arguments
   1. `@plz.task(requires=[lint, test])`
   2. `@plz.task(requires=[(lint, "arg1"), (test, "arg2")])`
   3. `@plz.task(requires=[lint, (test, ("arg1", "arg2"))])`
