from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AObserver(ABC):
    @abstractmethod
    def update(self, weather_data: Dict[str, Any]):
        pass

class ASubject(ABC):
    def __init__(self):
        self._observers: List[AObserver] = []

    def attach(self, observer: AObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: AObserver):
        self._observers.remove(observer)

    def notify(self, weather_data: Dict[str, Any]):
        for observer in self._observers:
            observer.update(weather_data)