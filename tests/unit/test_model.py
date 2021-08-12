from datetime import datetime, timedelta

import pytest

from scheduler.domain.model import Dependency, Event, EventType


@pytest.mark.parametrize(
    "event, valid",
    [
        (
            Event(
                type=EventType.FILE,
                resource_id="/foo/bar/baz",
                timestamp=datetime.utcnow() - timedelta(seconds=1800),
            ),
            True,
        ),
        (
            Event(
                type=EventType.FILE,
                resource_id="/foo",
                timestamp=datetime.utcnow() - timedelta(seconds=1800),
            ),
            False,
        ),
        (
            Event(
                type=EventType.FILE,
                resource_id="/foo/bar/baz",
                timestamp=datetime.utcnow() - timedelta(seconds=3601),
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
