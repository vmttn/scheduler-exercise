from datetime import timedelta

import pytest

from scheduler.adapters.configurations import CsvConfigurationRepository
from scheduler.domain.model import Configuration, Dependency, EventType
from scheduler.entrypoints.flask_app import app


@pytest.fixture
def api_client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def csv_config_repository():
    repo = CsvConfigurationRepository()
    yield repo
    repo._teardown()


@pytest.fixture
def scheduling_configuration_1(csv_config_repository: CsvConfigurationRepository):
    csv_config_repository.add(
        Configuration(
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
    )
    csv_config_repository._dump()
