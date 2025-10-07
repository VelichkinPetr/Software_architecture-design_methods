from abc import ABC, abstractmethod
import tkinter as tk


class ALabel(ABC):
    @abstractmethod
    def draw(self, parent, *args, **kwargs):
        raise NotImplementedError

class AButton(ABC):
    @abstractmethod
    def draw(self, parent, *args, **kwargs):
        raise NotImplementedError

class AEntry(ABC):
    @abstractmethod
    def draw(self, parent, *args, **kwargs):
        raise NotImplementedError

class AFrame(ABC):
    @abstractmethod
    def draw(self, parent, *args, **kwargs):
        raise NotImplementedError

class LightLabel(ALabel):

    def draw(self, parent, *args, **kwargs) -> tk.Label:
        base_config = {'bg': 'white', 'fg': 'black'}
        base_config.update(kwargs)
        return tk.Label(parent, **base_config)

class LightButton(AButton):

    def draw(self, parent, *args, **kwargs) -> tk.Button:
        base_config = {
            'bg': '#f0f0f0',
            'fg': 'black',
            'relief': 'raised',
            'bd': 2
        }
        base_config.update(kwargs)
        return tk.Button(parent, **base_config)

class LightEntry(AEntry):

    def draw(self, parent, *args, **kwargs) -> tk.Entry:
        base_config = {
            'bg': 'white',
            'fg': 'black',
            'relief': 'sunken',
            'bd': 2
        }
        base_config.update(kwargs)
        return tk.Entry(parent, **base_config)

class LightFrame(AFrame):

    def draw(self, parent, *args, **kwargs) -> tk.Frame:
        base_config = {'bg': 'white', 'relief': 'raised', 'bd': 1}
        base_config.update(kwargs)
        return tk.Frame(parent, **base_config)

class DarkLabel(ALabel):

    def draw(self, parent, *args, **kwargs) -> tk.Label:
        base_config = {'bg': '#2b2b2b', 'fg': 'white'}
        base_config.update(kwargs)
        return tk.Label(parent, **base_config)

class DarkButton(AButton):

    def draw(self, parent, *args, **kwargs) -> tk.Button:
        base_config = {
            'bg': '#404040',
            'fg': 'white',
            'relief': 'raised',
            'bd': 2
        }
        base_config.update(kwargs)
        return tk.Button(parent, **base_config)

class DarkEntry(AEntry):

    def draw(self, parent, *args, **kwargs) -> tk.Entry:
        base_config = {
            'bg': '#404040',
            'fg': 'white',
            'relief': 'sunken',
            'bd': 2
        }
        base_config.update(kwargs)
        return tk.Entry(parent, **base_config)

class DarkFrame(AFrame):

    def draw(self, parent, *args, **kwargs) -> tk.Frame:
        base_config = {'bg': '#2b2b2b', 'relief': 'raised', 'bd': 1}
        base_config.update(kwargs)
        return tk.Frame(parent, **base_config)