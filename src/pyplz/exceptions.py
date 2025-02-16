from abc import ABC, abstractmethod


class PlzError(Exception, ABC):
    @abstractmethod
    def verbose(self):
        pass


class ParsingError(PlzError):
    pass


class TaskDefinitionError(PlzError):
    pass


class PlzFileError(PlzError):
    pass


class TaskNotFoundError(ParsingError):
    def __init__(self, task_name: str):
        self.task_name = task_name

    def verbose(self):
        return f"Task not found: `{self.task_name}`"


class TypeAnnotationNotAllowed(TaskDefinitionError):
    def __init__(self, param_type_hint: str):
        self.param_type_hint = param_type_hint

    def verbose(self):
        return f"Type annotation `{self.param_type_hint}` is not allowed."


class ForwardRefrenceNotSupported(PlzFileError):
    def verbose(self):
        return (
            "Forward reference is not supported in type plzfile.\n"
            "This can happen when using `from __future__ import annotations`\n"
            "Or using a string as a type hint.\n"
            "Please use the actual type instead."
        )
