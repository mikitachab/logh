#!/usr/bin/env python3
import argparse
import datetime
import sys

import db
import printer
import utils

__version__ = '0.1.0'


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


def main():
    parser = argparse_parser_setup()
    args = parser.parse_args()

    if is_not_any_args_given():
        parser.print_help()
        exit()

    db.check_or_create_db()

    command, command_args = get_command(args)
    dispath(command, command_args)


def is_not_any_args_given():
    return not len(sys.argv) > 1


def dispath(command, args):
    command_to_handler = {
        'time': add_worktime,
        'list': list_all,
        'month': list_month,
        'remove_id': remove,
    }
    command_to_handler[command](args)


def add_worktime(worktime):
    db.insert_worktime(worktime)


def list_all(*args):
    worktimes = db.get_all_worktimes()
    printer.pretty_print_worktimes(worktimes)


def list_month(month):
    month = datetime.date.today().month
    month_worktimes = db.filter_by_month(month)
    month_sum = utils.calc_time_sum(month_worktimes)
    printer.pretty_print_worktimes(month_worktimes)
    printer.print_month_sum(month_sum)


def remove(id_):
    db.remove_worktime(id_)


if __name__ == '__main__':
    main()
