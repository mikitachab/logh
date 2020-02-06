#!/usr/bin/env python3
import argparse
import sys

import logh

__version__ = '0.2.0'


def argparse_parser_setup():
    parser = argparse.ArgumentParser(prog='logh', description='Tool for logging work hours')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--version', action='version', version='%(prog)s ' + __version__,
        help='print version of logh'
    )
    group.add_argument(
        '-a', dest='time', default=None, metavar='timestr',
        help='add work time in special format: <x>h<x>m, (e.g. 8h or 7h30m)'
    )
    group.add_argument(
        '-l', dest='list', default=None, action='store_true',
        help='list all added worktimes'
    )
    group.add_argument(
        '-m', dest='month', default=None, action='store_true',
        help=' list add hours if current month and calculate sum'
    )
    group.add_argument(
        '-r', dest='remove_id', default=None, metavar='id', type=int,
        help='remove worktime with given id'
    )
    return parser


def get_command(parsed_args):
    parsed_args = vars(parsed_args)
    command = [arg for arg, value in parsed_args.items() if value][0]
    return command, parsed_args[command]


def is_not_any_args_given():
    return not len(sys.argv) > 1


def main():
    parser = argparse_parser_setup()
    args = parser.parse_args()

    if is_not_any_args_given():
        parser.print_help()
        exit()

    command, command_args = get_command(args)
    logh.dispatch(command, command_args)


if __name__ == '__main__':
    main()
