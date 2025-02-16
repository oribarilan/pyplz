# Auto Help

`pyplz` offers dynamic help documentation, so your tasks get command-line documentation automatically.

## plz-level help

The `plz` command has a built-in help system. You can access it by running `plz -h` or `plz --help`. 

## task-level help

`pyplz` generates dynamic cli help documentation for your defined tasks.
Refrence it by running:

```bash
plz <some-task-name> -h
```

!!! tip "Tip"
    Task docstring will appear in the help documentation.