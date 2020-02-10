import datetime
import functools

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


def handler(*handler_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(args):
            if handler_args:
                func(*[args.get(arg) for arg in handler_args])
            else:
                func()
        return wrapper
    return decorator


@handler('time')
def add_worktime(worktime):
    if validator.validate_worktime(worktime):
        db.insert_worktime(worktime)
    else:
        print('Invalid worktime format, should be <x>h<x>m, (e.g. 8h or 7h30m)')


@handler()
def list_all():
    worktimes = db.get_all_worktimes()
    printer.pretty_print_worktimes(worktimes)


@handler()
def list_month():
    month = datetime.date.today().month
    month_worktimes = db.filter_by_month(month)
    month_sum = utils.calc_time_sum(month_worktimes)
    printer.pretty_print_worktimes(month_worktimes)
    printer.print_month_sum(month_sum)


@handler('remove_id')
def remove(id_):
    db.remove_worktime(id_)
