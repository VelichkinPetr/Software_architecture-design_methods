from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Callable


class AReaction(ABC):

    @abstractmethod
    def handler(self, observer: AObserver, subject: ASubject, data: Any):
        pass

class NewsReaction(AReaction):

    def handler(self, observer: AObserver, subject: ASubject, data: Any):
        print(f"НОВОСТИ {observer.name} получил уведомление {subject.name}: {data}")

class WeatherReaction(AReaction):

    def handler(self, observer: AObserver, subject: ASubject, data: Any):
        print(f"ПОГОДА {observer.name} получил уведомление {subject.name}: {data}")

class MusicReaction(AReaction):

    def handler(self, observer: AObserver, subject: ASubject, data: Any):
        print(f"МУЗЫКА {observer.name} получил уведомление {subject.name}: {data}")

class NonsenseReaction(AReaction):

    def handler(self, observer: AObserver, subject: ASubject, data: Any):
        print(f"ПОЛНАЯ ЧУШЬ {observer.name} получил уведомление {subject.name}: {data}")

class NonsenseReactionDmitry(AReaction):

    def handler(self, observer: AObserver, subject: ASubject, data: Any):
        print(f"{observer.name} получил уведомление {subject.name}: {data} .................КАРА!!!!!")

class AObserver(ABC):
    def __init__(self):
        self._subscriptions: List[ASubject] = []
        self._reactions: Dict[str, Callable] = {}

    @abstractmethod
    def update(self, subject: ASubject, data: Any):
        pass

    def subscribe_to(self, subject: ASubject, reaction: AReaction):
        subject.attach(self)
        self._reactions[subject.name] = reaction.handler
        self._subscriptions.append(subject.name)

    def unsubscribe_from(self, subject: ASubject):
        subject.detach(self)
        self._reactions.pop(subject.name)
        self._subscriptions.remove(subject.name)

class ASubject(ABC):
    def __init__(self):
        self._observers: List[AObserver] = []

    def attach(self, observer: AObserver):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: AObserver):
        self._observers.remove(observer)

    def notify(self, data: str):
        for observer in self._observers:
            observer.update(self, data)

class Publisher(ASubject):
    def __init__(self, name):
        super().__init__()
        self.name = name


class User(AObserver):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def update(self, subject, data):
        self._reactions[subject.name](self, subject, data)

    def subscribe_to(self, subject, reaction):
        super().subscribe_to(subject, reaction)
        print(f"{self.name} подписался на {subject.name}")

    def unsubscribe_from(self, subject):
        super().unsubscribe_from(subject)
        print(f"{self.name} отписался от {subject.name}")

#Издатели
news = Publisher("Новости")
weather = Publisher("Погода")
music = Publisher("Музыка")
nonsense = Publisher("Чушь...")

#Пользователь
user = User("Дмитрий")
user2 = User("Петр")

# Подписка на нескольких издателей
user.subscribe_to(news, NewsReaction())
user.unsubscribe_from(news)
user.subscribe_to(weather, WeatherReaction())
user.subscribe_to(music, MusicReaction())
user.subscribe_to(nonsense, NonsenseReactionDmitry())
print()
user2.subscribe_to(news, NewsReaction())
user2.subscribe_to(nonsense, NonsenseReaction())
print()

#Уведомления от издателей
news.notify("Беспилотная Опасность! Не выходите из домов!")
weather.notify("Погода сегодня: Вторник, 7.10.25, 25°C")
music.notify("Вышел новый музыкальный трек <...> Успей прослушать раньше всех!")
nonsense.notify("Полисорфизм == Наследование")
