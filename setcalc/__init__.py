from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path

from lark import Lark

from .transformation import SetCalcTransformer


def run() -> None:
    args = _parse_args()
    try:
        _run_command(args.grammar_file, args.command)
    except Exception as e:
        print(e)


def _parse_args() -> None:
    arg_parser = ArgumentParser(prog='setcalc')
    arg_parser.add_argument(
        '-g',
        '--grammar-file',
        required=False,
        default='grammar.txt',
        help=('the path to the file containing the description of the '
              'command\'s grammar'))

    arg_parser.add_argument(
        'command',
        nargs='+',
        metavar='REST',
        help='the text of the command to be executed')

    return arg_parser.parse_args()


def _run_command(file_path: str, command: list[str]) -> None:
    command = ' '.join(command)

    parser = Lark(
        (Path(__file__).absolute().parent / '..' / file_path).read_text(),
        start='expression',
        parser='lalr',
        transformer=SetCalcTransformer())
    result = parser.parse(command)

    for num in sorted(result):
        print(num)
