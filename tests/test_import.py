import os
import sys

from pyplz import plz
from pyplz.main import main


class TestMain:
    def test_import(self, tmp_path):
        other_module = """
import math

def my_square(x: int) -> int:
    return math.pow(x, 2)
"""

        plzfile_content = """
from pyplz import plz
from other_module import my_square


@plz.task()
def sample_task():
    my_square(2)
"""

        # temporarily create both files
        other_module_path = tmp_path / "other_module.py"
        plzfile_path = tmp_path / "plzfile.py"
        other_module_path.write_text(other_module)
        plzfile_path.write_text(plzfile_content)
        # sys.path.insert(0, str(tmp_path))
        # mock os.getcwd() to tmp_path
        os.getcwd = lambda: str(tmp_path)
        plz._internal_load_plzfile()

        sys.argv = ["plz", "sample-task"]

        main()
