from typing import Dict, List, Optional
from gettext import gettext as _

from gi.repository import Gio, GObject


class BaseRow(GObject.GObject):
    __gtype_name__ = "BaseRowModel"

    __items__: Dict[str, str] = {}

    value = GObject.Property(type=str)
    text = GObject.Property(type=str)

    def __init__(self, value: str, text: str) -> None:
        super().__init__()
        self.value = value
        self.text = text

    @classmethod
    def model(cls, default=False, exclude: Optional[List[str]] = None) -> Gio.ListStore:
        model = Gio.ListStore()

        if default is True:
            model.append(cls(value="default", text=_("Default")))

        for value, text in cls.__items__.items():
            if exclude is not None and value in exclude:
                continue
            model.append(cls(value=value, text=text))

        return model
