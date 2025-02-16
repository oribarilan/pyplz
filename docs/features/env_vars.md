# Environment Variables

## Defining Environment Variables
`pyplz` has extensive support for environment variables.

### .env file

`pyplz` will automatically load environment variables from a `.env` file in the same level of your `plzfile`.
Each line in the file should be in the format `KEY=VALUE`.

These variables will be available to all tasks (i.e., `plz-level`).

### Configuration

`pyplz` supports being configured from within the `plzfile` itself.
Among other things, you can define environment variables in the configuration.
For more information, see the [Configuration](./configuration.md) documentation.

These variables are `plz-level` as well.

```python
import os
from pyplz import plz

plz.configure(env={"a": "1", "b": "2"})

@plz.task()
def my_task():
    print(os.environ["a"])
```

### Task Definition

You can define environment variables for a specific task by using the `envs` parameter in the task definition.

```python
import os
from pyplz import plz

@plz.task(envs={"foo": "bar"})
def my_task():
    print(os.environ["foo"])
```

These variables will only be available to the task they are defined for (i.e., `task-level`).

### In-line

You can also define environment variables in-line when running a task, using the `-e` or `--env` flag per variable.

These variables are `task-level` as well.

For example:

```bash
plz -e VERBOSE=true -e DEBUG=true build
```

Note that in-line variables are defined before the task name, as can be seen in `plz -h`.

## Showing Environment Variables

You can see environment variables available to a task by using the `--show-env` (pyplz variables) or `--show-env-all` (all accessible variables) flags.