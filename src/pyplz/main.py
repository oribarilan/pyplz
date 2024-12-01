import sys

from pyplz.command import Parser
from pyplz.plz_app import plz


def main():
    parser = Parser()
    command = parser.parse_args(sys.argv[1:])

    plz._configure(parser=parser)

    plz._main_execute(command)
