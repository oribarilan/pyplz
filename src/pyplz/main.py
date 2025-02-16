import sys

from pyplz.error_handler import ErrorHandler
from pyplz.plz_app import plz
from pyplz.plz_parser import PlzParser
from pyplz.task_parser import TaskParser


def main():
    with ErrorHandler() as h:
        plz._load_plzfile()
        parser = PlzParser(plz_app=plz, task_parser=TaskParser())
        command = parser.parse(sys.argv[1:])

    if h.caught:
        sys.exit(1)

    plz._main_execute(command)


if __name__ == "__main__":
    main()
