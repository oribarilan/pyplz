import importlib.util
import os
import sys

from plz.plz_app import plz


def main():
    if len(sys.argv) < 2:
        task_name = None
    else:
        task_name = sys.argv[1]
    args = sys.argv[2:]

    plzfile_path = os.path.join(os.getcwd(), "plzfile.py")
    if not os.path.isfile(plzfile_path):
        print("No plzfile.py found in the current directory.")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("plzfile", plzfile_path)
    plzfile = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(plzfile)  # type: ignore

    plz._run_task(task_name, *args)
