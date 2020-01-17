import pytest

from validator import validate_worktime


@pytest.mark.parametrize('worktime, expected', [
    ('8h', True),
    ('7h30m', True),
    ('30m', True),
    ('4k6k', False),
])
def test_validate_worktime(worktime, expected):
    assert validate_worktime(worktime) == expected
