from pyplz.exceptions import PlzError
from pyplz.plz_app import PlzApp


class ErrorHandler:
    def __init__(self):
        self.caught = False

    def __enter__(self):
        # Any setup can be done here if needed
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            return False

        if issubclass(exc_type, PlzError):
            PlzApp.print_error(exc_value.verbose(), exit=True)

        # False to raise the unhandled exception
        return False
