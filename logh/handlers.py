import datetime

import logh.db as db
import logh.printer as printer
import logh.utils as utils
import logh.validator as validator


def get_handler(command):
    return {
        'time': add_worktime,
        'list': list_all,
        'month': list_month,
        'remove_id': remove,
    }[command]


def add_worktime(worktime):
    if validator.validate_worktime(worktime):
        db.insert_worktime(worktime)
    else:
        print('Invalid worktime format, should be <x>h<x>m, (e.g. 8h or 7h30m)')


def list_all(*args):  # TODO fix *args
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
