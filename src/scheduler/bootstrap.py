from scheduler.adapters.configurations import CsvConfigurationRepository


def bootstrap():
    CsvConfigurationRepository().dump()
