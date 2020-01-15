import re


WORKTIME_RE = r'([\d]+[hm]){1,2}'


def validate_worktime(worktime):
    return True if re.match(WORKTIME_RE, worktime) else False
