import importlib.util
import os
import sys

from plz.command import Parser
from plz.plz_app import plz


def main():
    parser = Parser()
    command = parser.parse_args(sys.argv[1:])

    plzfile_path = os.path.join(os.getcwd(), "plzfile.py")
    if not os.path.isfile(plzfile_path):
        plz.print("No plzfile.py found in the current directory.")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("plzfile", plzfile_path)
    plzfile = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(plzfile)  # type: ignore

    plz._configure(parser=parser)

    plz._main_execute(command)
