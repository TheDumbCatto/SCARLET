import argparse
import inspect
import sys
from typing import Optional

import pkg_resources
import shtab

from opera_tosca_parser import commands


class ArgParser(argparse.ArgumentParser):
    """An argument parser that displays help on error"""

    def error(self, message: str):
        """
        Overridden the original error method
        :param message: Error message
        """
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(1)

    def add_subparsers(self, **kwargs) -> argparse._SubParsersAction:
        """
        Overridden the original add_subparsers method (workaround for http://bugs.python.org/issue9253)
        :return: Subparsers action as argparse._SubParsersAction object
        """
        subparsers = super(ArgParser, self).add_subparsers()  # pylint: disable=super-with-arguments
        subparsers.required = True
        subparsers.dest = "command"
        return subparsers


class PrintCurrentVersionAction(argparse.Action):
    """Action for printing current package version"""

    def __call__(self, parser: ArgParser, namespace: argparse.Namespace, values: list,
                 option_string: Optional[str] = None):
        """
        Overridden the call action method
        :param parser: Argument parser
        :param namespace: Namespace as argparse.Namespace
        :param values: List of values
        :param option_string: Option string
        """
        try:
            print(pkg_resources.get_distribution("opera-tosca-parser").version)
            parser.exit(0)
        except pkg_resources.DistributionNotFound as e:
            print(f"Error when retrieving current opera-tosca-parser version: {e}")
            parser.exit(1)


def create_parser() -> ArgParser:
    """
    Create argument parser for CLI
    :return: Parser as argparse.ArgumentParser object
    """
    parser = ArgParser(
        description="xOpera TOSCA parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # use shtab magic and add global optional argument for generating shell completion script
    shtab.add_argument_to(
        parser, ["-s", "--shell-completion"],
        help="Generate tab completion script for your shell"
    )
    # add global optional argument for printing current package version
    parser.add_argument(
        "--version", "-v", action=PrintCurrentVersionAction, nargs=0, help="Retrieve current opera-tosca-parser version"
    )

    subparsers = parser.add_subparsers()
    cmds = inspect.getmembers(commands, inspect.ismodule)
    for _, module in sorted(cmds, key=lambda x: x[0]):
        module.add_parser(subparsers)
    return parser


def main() -> ArgParser:
    """
    The main CLI method to be called
    :return: Parser as argparse.ArgumentParser object
    """
    parser = create_parser()
    args = parser.parse_args()
    return args.func(args)
