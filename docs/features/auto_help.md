# Auto Help

## plz-level help

The `plz` command has a built-in help system. You can access it by running `plz -h` or `plz --help`. 

This will include:
* Usage pattern
* Available flags
* Available tasks
* Plz-level Environment variables (for more info on environment variables, see [Environment Variables](./env_vars.md))

## task-level help

You can also get help for a specific task by running `plz -h <task-name>` or `plz --help <task-name>`.

This will display more detailed information about the task, including:
* Dependencies
* Description
* Parameters
* Task-level Environment variables (for more info on environment variables, see [Environment Variables](./env_vars.md))