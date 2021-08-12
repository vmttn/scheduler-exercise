import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Mapping, Optional

from scheduler.utils.time import get_time

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    FILE = "FILE"
    TIME_BASED = "TIME_BASED"
    TABLE = "TABLE"


@dataclass(frozen=True)
class Event:
    type: EventType
    resource_id: str
    timestamp: datetime


@dataclass(frozen=True)
class Dependency:
    type: EventType
    resource_id: str
    life_duration: timedelta

    def validate(self, event: Event) -> bool:
        return event.type is self.type and VALIDATORS[self.type].validate(self, event)


class DependencyValidator:
    def validate(self, dependency: Dependency, event: Event) -> bool:
        return self.validate_time(dependency, event) and self.validate_extra(dependency, event)

    def validate_time(self, dependency: Dependency, event: Event):
        return (
            dependency.life_duration.total_seconds() == 0 or get_time() - event.timestamp <= dependency.life_duration
        )

    def validate_extra(self, dependency: Dependency, event: Event) -> bool:
        return True


class FileDependencyValidator(DependencyValidator):
    def validate_extra(self, dependency: Dependency, event: Event) -> bool:
        return event.resource_id.startswith(dependency.resource_id)


class TimeBasedDependencyValidator(DependencyValidator):
    pass


class TableDependencyValidator(DependencyValidator):
    pass


VALIDATORS: Mapping[EventType, DependencyValidator] = {
    EventType.FILE: FileDependencyValidator(),
    EventType.TIME_BASED: TimeBasedDependencyValidator(),
    EventType.TABLE: TableDependencyValidator(),
}


class Configuration:
    def __init__(self, name: str, dependencies: List[Dependency]) -> None:
        self.name = name
        self.dependencies = dependencies
        self._last_execution: Optional[datetime] = None
        self._last_match_by_dependency: Dict[Dependency, Event] = {}

    def find_matchs(self, event: Event) -> List[Dependency]:
        return [d for d in self.dependencies if d.validate(event)]

    def update_last_matchs(self, event: Event) -> None:
        matching_dependencies = self.find_matchs(event)

        for dependency in matching_dependencies:
            if (
                dependency not in self._last_match_by_dependency
                or self._last_match_by_dependency[dependency].timestamp < event.timestamp
            ):
                self._last_match_by_dependency[dependency] = event

    def validate(self) -> bool:
        return all(
            [
                d.validate(self._last_match_by_dependency[d]) if d in self._last_match_by_dependency else False
                for d in self.dependencies
            ]
        )

    def process(self, event: Event) -> bool:
        if self._last_execution is None or event.timestamp > self._last_execution:
            self.update_last_matchs(event)
            if self.validate():
                self.execute()
                return True
        return False

    def execute(self):
        logger.info("Executing...")
        self._last_execution = get_time()
