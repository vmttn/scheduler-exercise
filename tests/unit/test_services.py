from datetime import datetime
from typing import List

from dateutil import tz

from scheduler.adapters.configurations import FakeConfigurationRepository
from scheduler.domain.model import Configuration, Event, EventType
from scheduler.service_layer import services
from scheduler.utils.time import get_tz_time


def test_process_event_001(scheduling_configuration_1: Configuration):
    configurations = FakeConfigurationRepository([scheduling_configuration_1])
    file_event = Event(
        type=EventType.FILE,
        resource_id="/scheduling_configuraiton_1/directory/path/foo",
        timestamp=get_tz_time(),
    )
    time_based_event = Event(
        type=EventType.TIME_BASED,
        resource_id="cron",
        timestamp=get_tz_time(),
    )

    services.process_event(configurations, file_event)
    assert configurations.get(scheduling_configuration_1.name)._last_execution is None
    services.process_event(configurations, time_based_event)
    assert configurations.get(scheduling_configuration_1.name)._last_execution is not None


class FakeTime:
    """Callable used to control the application time."""

    def __init__(self, datetimes: List[datetime]) -> None:
        self._dt = datetimes

    def forward(self):
        self._dt.pop(0)

    def __call__(self) -> datetime:
        return self._dt[0]


def test_can_reproduce_scenario(scheduling_configuration_1: Configuration):
    configurations = FakeConfigurationRepository([scheduling_configuration_1])

    fake_time = FakeTime(
        [
            datetime(2020, 1, 1, 12, 0, 0, tzinfo=tz.tzlocal()),
            datetime(2020, 1, 1, 12, 5, 0, tzinfo=tz.tzlocal()),
            datetime(2020, 1, 1, 12, 15, 0, tzinfo=tz.tzlocal()),
            datetime(2020, 1, 1, 12, 15, 30, tzinfo=tz.tzlocal()),
            datetime(2020, 1, 1, 12, 30, 1, tzinfo=tz.tzlocal()),
            datetime(2020, 1, 1, 13, 10, 1, tzinfo=tz.tzlocal()),
            datetime(2020, 1, 1, 13, 30, 1, tzinfo=tz.tzlocal()),
        ]
    )

    from scheduler.utils import time

    time.DEFAULT_TIME_FN = fake_time

    events = [
        (
            Event(
                type=EventType.FILE,
                resource_id="/scheduling_configuraiton_1/directory/path/file_1.txt",
                timestamp=datetime(2020, 1, 1, 11, 59, 59, tzinfo=tz.tzlocal()),
            ),
            scheduling_configuration_1.dependencies[0],
            False,
        ),
        (
            Event(
                type=EventType.FILE,
                resource_id="/scheduling_configuraiton_1/directory/path/file_2.txt",
                timestamp=datetime(2020, 1, 1, 12, 4, 59, tzinfo=tz.tzlocal()),
            ),
            scheduling_configuration_1.dependencies[0],
            False,
        ),
        (
            Event(
                type=EventType.FILE,
                resource_id="/scheduling_configuraiton_1/directory/path/file_3.txt",
                timestamp=datetime(2020, 1, 1, 12, 14, 50, tzinfo=tz.tzlocal()),
            ),
            scheduling_configuration_1.dependencies[0],
            False,
        ),
        (
            Event(
                type=EventType.FILE,
                resource_id="/scheduling_configuraiton_1/directory/an_other_path/file_3.txt",
                timestamp=datetime(2020, 1, 1, 12, 15, 28, tzinfo=tz.tzlocal()),
            ),
            None,
            False,
        ),
        (
            Event(
                type=EventType.TIME_BASED,
                resource_id="cron",
                timestamp=datetime(2020, 1, 1, 12, 30, 0, tzinfo=tz.tzlocal()),
            ),
            scheduling_configuration_1.dependencies[1],
            True,
        ),
        (
            Event(
                type=EventType.TIME_BASED,
                resource_id="cron",
                timestamp=datetime(2020, 1, 1, 13, 10, 0, tzinfo=tz.tzlocal()),
            ),
            scheduling_configuration_1.dependencies[1],
            True,
        ),
        (
            Event(
                type=EventType.TIME_BASED,
                resource_id="cron",
                timestamp=datetime(2020, 1, 1, 13, 30, 0, tzinfo=tz.tzlocal()),
            ),
            scheduling_configuration_1.dependencies[1],
            False,
        ),
    ]

    for event, dependency_validated, job_triggered in events:
        config_validated = services.process_event(configurations, event)

        # Check if a job has been triggered
        assert job_triggered == (len(config_validated) > 0), f"<time={fake_time()}, event={event}>"
        # Check if the event has validated a dependency
        assert (
            dependency_validated is None
            or scheduling_configuration_1._last_match_by_dependency[dependency_validated] == event
        )
        # Move time forward
        fake_time.forward()
