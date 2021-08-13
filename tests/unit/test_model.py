from datetime import timedelta

import pytest

from scheduler.domain.model import Dependency, Event, EventType
from scheduler.utils.time import get_tz_time


@pytest.mark.parametrize(
    "event, valid",
    [
        (
            Event(
                type=EventType.FILE,
                resource_id="/foo/bar/baz",
                timestamp=get_tz_time() - timedelta(seconds=1800),
            ),
            True,
        ),
        (
            Event(
                type=EventType.FILE,
                resource_id="/foo",
                timestamp=get_tz_time() - timedelta(seconds=1800),
            ),
            False,
        ),
        (
            Event(
                type=EventType.FILE,
                resource_id="/foo/bar/baz",
                timestamp=get_tz_time() - timedelta(seconds=3601),
            ),
            False,
        ),
    ],
)
def test_file_based_validation(event, valid):
    dependency = Dependency(
        type=EventType.FILE,
        resource_id="/foo/bar",
        life_duration=timedelta(seconds=3600),
    )
    assert dependency.validate(event) == valid
