def pretty_print_worktimes(worktimes):
    row_format = '|{:^4}|{:^12}|{:^8}|'
    print('-' * 28)
    print(row_format.format('id', 'day', 'time'))
    print('|' + '-' * 4 + '|' + '-' * 12 + '|' + '-' * 8 + '|')
    for id_, workday, time_ in worktimes:
        print(row_format.format(id_, workday, time_))
    print('-' * 28)


def print_month_sum(month_sum):
    print('SUM  ', month_sum[0], 'h', month_sum[1], 'm',)
