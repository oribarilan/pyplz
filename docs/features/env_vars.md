# Environment Variables

`pyplz` has extensive support for environment variables.

## .env file

`pyplz` will automatically load environment variables from a `.env` file in the root of your project. 
Each line in the file should be in the format `KEY=VALUE`.

These variables will be available to all tasks (i.e., `plz-scope`).

## Configuration

`pyplz` supports a being configured from within the `plzfile` itself.
Among other things, you can define environment variables in the configuration.
For more information, see the [Configuration](./configuration.md) documentation.

These variables are `plz-scope` as well.

## Task Definition

You can define environment variables for a specific task by adding a `env` key to the task definition.

These variables will only be available to the task they are defined for (i.e., `task-scope`).

## In-line

You can also define environment variables in-line when running a task, using the `-e` or `--env` flag per variable.

These variables are `task-scope` as well.

For example:

```bash
plz -e VERBOSE=true -e DEBUG=true build
```