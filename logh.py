#!/usr/bin/env python3
import argparse
import datetime
import sys
import re

import db
import printer

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


def calc_time_sum(worktimes):
    def parse_time(timestr, units):
        """units 'h' or 'm'"""
        match = re.search(r'(\d+){}'.format(units), timestr)
        if match:
            return int(match.group(1))
        return 0

    hours = sum([parse_time(worktime[2], 'h') for worktime in worktimes])
    minutes = sum([parse_time(worktime[2], 'm') for worktime in worktimes])

    more_hours = minutes // 60
    if more_hours > 0:
        hours += more_hours
        minutes = minutes % 60

    return hours, minutes


def main():
    parser = argparse_parser_setup()
    args = parser.parse_args()

    if not len(sys.argv) > 1:
        parser.print_help()
        exit()

    db.check_or_create_db()

    if args.time:
        db.insert_worktime(args.time)

    if args.list:
        worktimes = db.get_all_worktimes()
        printer.pretty_print_worktimes(worktimes)

    if args.remove_id:
        db.remove_worktime(args.remove_id)

    if args.month:
        month = datetime.date.today().month
        month_worktimes = db.filter_by_month(month)
        month_sum = calc_time_sum(month_worktimes)
        printer.pretty_print_worktimes(month_worktimes)
        printer.print_month_sum(month_sum)


if __name__ == '__main__':
    main()
