from typing import List

from scheduler.domain.model import Configuration


class ConfigurationRepository:
    def get(self, name) -> Configuration:
        raise NotImplementedError

    def list(self) -> List[Configuration]:
        raise NotImplementedError


class FakeConfigurationRepository(ConfigurationRepository):
    def __init__(self, configs: List[Configuration]) -> None:
        self._configs = set(configs)

    def get(self, name) -> Configuration:
        return next(c for c in self._configs if c.name == name)

    def list(self) -> List[Configuration]:
        return list(self._configs)
