from datetime import timedelta

import pytest

from scheduler.domain.model import Configuration, Dependency, EventType


@pytest.fixture
def scheduling_configuration_1():
    return Configuration(
        name="SCHEDULING_CONFIGURATION_1",
        dependencies=[
            Dependency(
                type=EventType.FILE,
                resource_id="/scheduling_configuraiton_1/directory/path/",
                life_duration=timedelta(seconds=3600),
            ),
            Dependency(
                type=EventType.TIME_BASED,
                resource_id="cron",
                life_duration=timedelta(),
            ),
        ],
    )


@pytest.fixture
def scheduling_configuration_2():
    return Configuration(
        name="SCHEDULING_CONFIGURATION_2",
        dependencies=[
            Dependency(
                type=EventType.TABLE,
                resource_id="BIGQUERY_TABLE_NAME_1",
                life_duration=timedelta(seconds=86400),
            ),
            Dependency(
                type=EventType.TABLE,
                resource_id="BIGQUERY_TABLE_NAME_2",
                life_duration=timedelta(seconds=86400),
            ),
            Dependency(
                type=EventType.TIME_BASED,
                resource_id="cron",
                life_duration=timedelta(),
            ),
        ],
    )


@pytest.fixture
def scheduling_configuration_3():
    return Configuration(
        name="SCHEDULING_CONFIGURATION_3",
        dependencies=[
            Dependency(
                type=EventType.TABLE,
                resource_id="BIGQUERY_TABLE_NAME_3",
                life_duration=timedelta(seconds=86400),
            ),
            Dependency(
                type=EventType.TABLE,
                resource_id="BIGQUERY_TABLE_NAME_4",
                life_duration=timedelta(),
            ),
        ],
    )
