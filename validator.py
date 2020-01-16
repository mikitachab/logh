import re

from constants import WORKTIME_RE


def validate_worktime(worktime):
    return True if re.match(WORKTIME_RE, worktime) else False
