import csv
import shutil
from pathlib import Path
from typing import Dict, List

from scheduler import settings
from scheduler.domain.model import Configuration, Dependency, Event


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


class CsvConfigurationRepository(ConfigurationRepository):
    def __init__(self, folder: Path = settings.CSV_REPOSITORY_FOLDER) -> None:
        self._folder = folder
        self._configs: Dict[str, Configuration] = {}
        self._load()

    def _ensure_files(self):
        self._folder.mkdir(parents=True, exist_ok=True)
        (self._folder / "configurations.csv").touch(exist_ok=True)
        (self._folder / "dependencies.csv").touch(exist_ok=True)

    def _load(self):
        self._ensure_files()

        with (self._folder / "configurations.csv").open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                config = Configuration.from_csv(row)
                self._configs[config.name] = config

        with (self._folder / "dependencies.csv").open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                config = self._configs[row["config_name"]]
                dependency = Dependency.from_csv(row)
                config.dependencies.append(dependency)
                if row["timestamp"]:
                    config._last_match_by_dependency[dependency] = Event.from_csv(row)

    def add(self, config: Configuration):
        self._configs[config.name] = config

    def dump(self):
        self._ensure_files()

        with (self._folder / "configurations.csv").open("w") as f:
            writer = csv.DictWriter(f, ["name", "last_execution"])
            writer.writeheader()
            for config in self._configs.values():
                writer.writerow(
                    {
                        "name": config.name,
                        "last_execution": config._last_execution.isoformat()
                        if config._last_execution is not None
                        else None,
                    }
                )
        with (self._folder / "dependencies.csv").open("w") as f:
            writer = csv.DictWriter(f, ["config_name", "type", "resource_id", "life_duration", "timestamp"])
            writer.writeheader()
            for config in self._configs.values():
                for dependency in config.dependencies:

                    writer.writerow(
                        {
                            "config_name": config.name,
                            "type": dependency.type.value,
                            "resource_id": dependency.resource_id,
                            "life_duration": dependency.life_duration.seconds,
                            "timestamp": config._last_match_by_dependency[dependency].timestamp.isoformat()
                            if dependency in config._last_match_by_dependency
                            else None,
                        }
                    )

    def get(self, name) -> Configuration:
        return self._configs[name]

    def list(self) -> List[Configuration]:
        return list(self._configs.values())

    def _teardown(self):
        shutil.rmtree(self._folder)
