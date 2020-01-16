import re


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
