from typing import List

from scheduler.adapters.configurations import ConfigurationRepository
from scheduler.domain.model import Configuration, Event


def process_event(
    configuration: ConfigurationRepository,
    event: Event,
) -> List[Configuration]:
    configurations_validated = []
    for config in configuration.list():
        if config.process(event):
            configurations_validated.append(config)

    return configurations_validated
