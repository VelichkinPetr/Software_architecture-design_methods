from WeatherInformer.src.GUI.products import *
import tkinter as tk
from abc import ABC, abstractmethod

class AWidgetFactory(ABC):
    @abstractmethod
    def create_label(self, parent, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create_button(self, parent, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create_entry(self, parent, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create_frame(self, parent, **kwargs):
        raise NotImplementedError


class LightThemeFactory(AWidgetFactory):
    def create_label(self, parent, *args, **kwargs) -> tk.Label:
        return LightLabel().draw(parent, *args, **kwargs)

    def create_button(self, parent, *args, **kwargs) -> tk.Button:
        return LightButton().draw(parent, *args, **kwargs)

    def create_entry(self, parent, *args, **kwargs) -> tk.Entry:
        return LightEntry().draw(parent, *args, **kwargs)

    def create_frame(self, parent, *args, **kwargs) -> tk.Frame:
        return LightFrame().draw(parent, *args, **kwargs)


class DarkThemeFactory(AWidgetFactory):
    def create_label(self, parent, *args, **kwargs) -> tk.Label:
        return DarkLabel().draw(parent, *args, **kwargs)

    def create_button(self, parent, *args, **kwargs) -> tk.Button:
        return DarkButton().draw(parent, *args, **kwargs)

    def create_entry(self, parent, *args, **kwargs) -> tk.Entry:
        return DarkEntry().draw(parent, *args, **kwargs)

    def create_frame(self, parent, *args, **kwargs) -> tk.Frame:
        return DarkFrame().draw(parent, *args, **kwargs)