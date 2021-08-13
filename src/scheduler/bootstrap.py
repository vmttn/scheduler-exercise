import logging

from scheduler import settings
from scheduler.adapters.configurations import CsvConfigurationRepository


def bootstrap():
    logging.basicConfig(level=settings.LOG_LEVEL)

    CsvConfigurationRepository().dump()  # Ensure CSVs exist
